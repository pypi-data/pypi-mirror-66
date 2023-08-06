"""Implementation of Padé based on robust pole finding.

Check scaling: 3.5.2, replace 2-norm by infty norm."""
from typing import NamedTuple

import numpy as np
import scipy.linalg as spla
import scipy.optimize as spopt
import scipy.odr

from numpy.polynomial import polynomial, Polynomial
from numpy import newaxis

import gftool as gt
import gftool.linalg


RatPol: NamedTuple  # define for later use


class PoleGf(NamedTuple):
    poles: np.ndarray
    resids: np.ndarray

    def evalz(self, z):
        return gt.pole_gf_z(z, poles=self.poles, weights=self.resids)

    def to_ratpol(self) -> 'RatPol':
        return RatPol.from_poles(poles=self.poles, resid=self.resids)


class RatPol(NamedTuple):
    """Rational polynomial given as numerator and denominator."""

    numer: Polynomial
    denom: Polynomial

    def __call__(self, z):
        return self.numer(z)/self.denom(z)

    @classmethod
    def from_poles(cls, poles, resid):
        assert poles.size == resid.size
        # get common denominator
        denom = Polynomial.fromroots(poles)
        numer = Polynomial([0])
        numbers = np.arange(poles.size)

        for idx in range(poles.size):
            # add expanded numinator
            numer += resid[idx]*Polynomial.fromroots(poles[numbers != idx])
        return cls(numer, denom)


def number_poles(z, fct_z, *, M_min_N=1, weight=False, M_start=50, vandermond=polynomial.polyvander):
    """Estimate the optimal number of poles for a rational approximation.

    Parameters
    ----------
    z, fct_z : (N_z) complex np.ndarray
        Variable where function is evaluated and function values.
    M_min_N : int, optional
        The difference of denominator and numerator degree. (default: 1)
    weight : (N_z) float np.ndarray, optional
        Weighting of the data points, for a known error `σ` this should be
        `weight = 1./σ`.
    M_start : int, optional
        Starting guess for the number of poles. Can be given to speed up
        calculation if a good estimate is available.
    vandermond : Callable, optional
        Function giving the Vandermond matrix of the chosen polynomial basis.

    Returns
    -------
    number_poles : int
        Best guess for optimal number of poles.

    """
    tol = np.finfo(fct_z.dtype).eps
    max_n_poles = abs_max_n_poles = (z.size + M_min_N)//2
    n_poles = M_start
    n_roots = n_poles - M_min_N
    assert n_poles <= max_n_poles
    assert n_poles + n_roots < z.size
    while True:
        n_roots = n_poles - M_min_N
        vander = vandermond(z, deg=max(n_poles, n_roots)+1)
        fct_denom = fct_z[:, np.newaxis]*vander[..., :n_poles+1]
        numer = vander[..., :n_roots+1]
        # TODO: check if [fct_denom, numer] is the better choice
        scaling = 1./np.linalg.norm(numer, axis=-1, keepdims=True)
        # FIXME
        scaling = 1./np.linalg.norm(np.concatenate((vander[..., :n_poles+1], numer), axis=-1), axis=-1, keepdims=True)
        if np.any(weight):
            scaling *= weight[..., np.newaxis]
        q_fct_x_denom, __ = np.linalg.qr(scaling*fct_denom)
        q_numer, __ = np.linalg.qr(scaling*numer)
        mat = np.concatenate([q_fct_x_denom, q_numer], axis=-1)
        singular_values = np.linalg.svd(mat, compute_uv=False)
        null_dim = np.count_nonzero(singular_values < tol*singular_values[0]*max(mat.shape))
        if null_dim == 1:  # correct number of poles
            # import matplotlib.pyplot as plt

            # plt.plot(singular_values, 'x--')
            # plt.yscale('log')
            # plt.show()
            return n_poles
        if null_dim == 0:  # too few poles
            if n_poles == abs_max_n_poles:
                raise RuntimeError(
                    f"No solution with {abs_max_n_poles} poles or less could be found!"
                )
            if n_poles == max_n_poles:
                print("Warning: residue is bigger then tolerance: "
                      f"{singular_values[-1]/singular_values[0]}.")
                return n_poles
            # increase number of poles
            n_poles = min(2*n_poles, max_n_poles)
        else:  # already too many poles
            max_n_poles = n_poles - 1
            n_poles = n_poles - (null_dim + M_min_N)//2


def poles(z, fct_z, *, N: int = None, M: int, vandermond=polynomial.polyvander, weight=False):
    """Calculate position of `M` poles.

    Parameters
    ----------
    z, fct_z : (N_z) complex np.ndarray
        Variable where function is evaluated and function values.
    N, M : int
        Number of roots and poles of the function.
        For large `z` the function is proportional to `z**(N - M)`.
        (`N` defaults to `M-1`)
    vandermond : Callable, optional
        Function giving the Vandermond matrix of the chosen polynomial basis.
    weight : (N_z) float np.ndarray, optional
        Weighting of the data points, for a known error `σ` this should be
        `weight = 1./σ`.

    Returns
    -------
    poles : (M) complex np.ndarray
        The position of the poles.

    """
    if N is None:
        N = M - 1
    fct_z = fct_z/np.median(fct_z)
    vander = vandermond(z, deg=max(N+1, M))
    numer = -vander[..., :N+1]
    fct_denom = fct_z[..., np.newaxis]*vander[..., :M]
    scaling = 1./np.linalg.norm(fct_denom, axis=-1, keepdims=True)
    # FIXME
    # scaling = 1./np.linalg.norm(np.concatenate((vander[..., :M], numer), axis=-1), axis=-1, keepdims=True)
    if np.any(weight):
        scaling *= weight[..., np.newaxis]
    q_numer, __ = np.linalg.qr(scaling*numer, mode='complete')
    q_fct_denom, __ = np.linalg.qr(scaling*fct_denom, mode='reduced')
    # q_fct_denom, *__ = spla.qr(D*B1, mode='economic', pivoting=True)
    qtilde_z_fct_denom = q_numer[..., N+1:].T.conj() @ (z[..., np.newaxis] * q_fct_denom)
    qtilde_fct_denom = q_numer[..., N+1:].T.conj() @ q_fct_denom
    __, __, vh = np.linalg.svd(np.concatenate((qtilde_z_fct_denom, qtilde_fct_denom), axis=-1))
    return spla.eig(vh[:M, :M], vh[:M, M:], right=False)


def roots(z, fct_z, poles, *, N: int = None, vandermond=polynomial.polyvander, weight=False):
    """Calculate position of `N` roots given the `poles`.

    Parameters
    ----------
    z, fct_z : (N_z) complex np.ndarray
        Variable where function is evaluated and function values.
    poles : (M) complex np.ndarray
        Position of the poles of the function
    N : int
        Number of roots.
        For large `z` the function is proportional to `z**(N - M)`.
        (`N` defaults to `M-1`)
    vandermond : Callable, optional
        Function giving the Vandermond matrix of the chosen polynomial basis.
    weight : (N_z) float np.ndarray, optional
        Weighting of the data points, for a known error `σ` this should be
        `weight = 1./σ`.

    Returns
    -------
    roots : (N) complex np.ndarray
        The position of the roots.

    """
    M = poles.size
    if N is None:
        N = M - 1
    fct_z = fct_z/np.median(fct_z)
    denom = np.prod(np.subtract.outer(z, poles), axis=-1)
    fct_denom = (fct_z*denom)[:, np.newaxis]
    numer = vandermond(z, deg=N-1)
    # scaling = 1./np.linalg.norm(fct_denom, axis=-1, keepdims=True)
    # FIXME
    # scaling = 1./np.linalg.norm(np.concatenate((denom[..., np.newaxis], numer), axis=-1), axis=-1, keepdims=True)  # this is terrible in practice!
    scaling = 1./np.linalg.norm(numer, axis=-1, keepdims=True)  # <- by far best
    if np.any(weight):
        scaling *= weight[..., np.newaxis]
    q_fct_denom, __ = np.linalg.qr(scaling*fct_denom, mode='complete')
    q_numer, __ = np.linalg.qr(scaling*numer, mode='reduced')
    qtilde_z_numer = q_fct_denom[:, 1:].T.conj() @ (z[..., np.newaxis] * q_numer)
    qtilde_numer = q_fct_denom[:, 1:].T.conj() @ q_numer
    __, __, vh = np.linalg.svd(np.concatenate((qtilde_z_numer, qtilde_numer), axis=-1))
    return spla.eig(vh[:N, :N], vh[:N, N:], right=False)


def opt_poles(z, fct_z, pole_gf: PoleGf, vandermond=polynomial.polyvander, weight=False):
    numer = -pole_gf.to_ratpol().numer(z)
    M = pole_gf.poles.shape[-1]
    fct_z = fct_z/np.median(fct_z)
    fct_denom = fct_z[:, np.newaxis] * vandermond(z, deg=M-1)
    scaling = 1./np.linalg.norm(fct_denom, axis=-1, keepdims=True)
    # FIXME
    scaling = 1./np.linalg.norm(np.concatenate((fct_denom, numer[..., newaxis]), axis=-1), axis=-1, keepdims=True)
    if np.any(weight):
        scaling *= weight[..., newaxis]
    q_numer, __ = np.linalg.qr(scaling*numer[..., newaxis], mode='complete')
    q_fct_denom, __ = np.linalg.qr(scaling*fct_denom, mode='reduced')
    qtilde_z_fct_denom = q_numer[:, 1:].T.conj() @ (z[..., newaxis] * q_fct_denom)
    qtilde_fct_denom = q_numer[:, 1:].T.conj() @ q_fct_denom
    __, __, vh = np.linalg.svd(np.concatenate((qtilde_z_fct_denom, qtilde_fct_denom), axis=-1))
    return spla.eig(vh[:M, :M], vh[:M, M:], right=False)


def residues_ols(z, fct_z, poles, weight=False):
    """Calculate the residues using ordinary least square.

    Parameters
    ----------
    z, fct_z : (N_z) complex np.ndarray
        Variable where function is evaluated and function values.
    poles : (M) complex np.ndarray
        Position of the poles of the function
    weight : (N_z) float np.ndarray, optional
        Weighting of the data points, for a known error `σ` this should be
        `weight = 1./σ`.

    Returns
    -------
    residues : (M) complex np.ndarray
        The residues corresponding to the `poles`.

    """
    polematrix = 1./np.subtract.outer(z, poles)
    if np.any(weight):
        polematrix *= weight[..., np.newaxis]
        fct_z = fct_z*weight
    return np.linalg.lstsq(polematrix, fct_z, rcond=None)[:2]


def residues_ols_tau(tau, fct_tau, poles, beta, weight=False):
    """Calculate the residues using ordinary least square.

    Parameters
    ----------
    z, fct_z : (N_z) complex np.ndarray
        Variable where function is evaluated and function values.
    poles : (M) complex np.ndarray
        Position of the poles of the function
    weight : (N_z) float np.ndarray, optional
        Weighting of the data points, for a known error `σ` this should be
        `weight = 1./σ`.

    Returns
    -------
    residues : (M) complex np.ndarray
        The residues corresponding to the `poles`.

    """
    polematrix_tau = gt.pole_gf_tau(tau, weights=1, poles=poles[:, np.newaxis], beta=beta)
    assert polematrix_tau.shape == tau.shape + poles.shape
    # polematrix = 1./np.subtract.outer(z, poles)
    if np.any(weight):
        # polematrix *= weight[..., np.newaxis]
        polematrix_tau *= weight[..., np.newaxis]
        fct_tau = fct_tau*weight
    return np.linalg.lstsq(polematrix_tau, fct_tau, rcond=None)[:2]


def residues_ols_tau_b(tau, fct_tau, poles, beta, weight=False):
    """Calculate the residues using ordinary least square.

    Parameters
    ----------
    z, fct_z : (N_z) complex np.ndarray
        Variable where function is evaluated and function values.
    poles : (M) complex np.ndarray
        Position of the poles of the function
    weight : (N_z) float np.ndarray, optional
        Weighting of the data points, for a known error `σ` this should be
        `weight = 1./σ`.

    Returns
    -------
    residues : (M) complex np.ndarray
        The residues corresponding to the `poles`.

    """
    polematrix_tau = gt.pole_gf_tau_b(tau, weights=1, poles=poles[:, np.newaxis], beta=beta)
    assert polematrix_tau.shape == tau.shape + poles.shape
    # polematrix = 1./np.subtract.outer(z, poles)
    if np.any(weight):
        # polematrix *= weight[..., np.newaxis]
        polematrix_tau *= weight[..., np.newaxis]
        fct_tau = fct_tau*weight
    return np.linalg.lstsq(polematrix_tau, fct_tau, rcond=None)[:2]


def residues_hybr_ols(z, fct_z, tau, fct_tau, poles, beta, moments=(), weight=False, weight_ratio=[.5, .5]):
    """Calculate residues fitting Matsubara as well as imaginary time data."""
    polematrix_z = 1./np.subtract.outer(z, poles)
    polematrix_tau = gt.pole_gf_tau(tau[:, newaxis], weights=1, poles=poles[:, newaxis], beta=beta)
    polemat = np.concatenate((polematrix_z, polematrix_tau), axis=-2)
    funcvec = np.concatenate((fct_z, fct_tau), axis=-1)
    scaling = 1./np.linalg.norm(polemat, axis=-1, keepdims=True)
    scaling = np.ones_like(polemat)
    if np.any(weight):
        scaling *= weight[..., np.newaxis]
    polemat *= scaling
    funcvec *= scaling[..., 0]

    # weight fct_z/fct_tau according to weight_ratio:
    rows = polemat.shape[-2]
    polemat[:z.size] *= weight_ratio[0] * rows / z.size  # weight of z data
    funcvec[:z.size] *= weight_ratio[0] * rows / z.size  # weight of z data
    polemat[z.size:] *= weight_ratio[1] * rows / tau.size  # weight of tau data
    funcvec[z.size:] *= weight_ratio[1] * rows / tau.size  # weight of tau data
    if moments:  # FIXME: allow also other constrains, like occupation Number
        moments = np.array(moments)
        constrain_mat = np.polynomial.polynomial.polyvander(poles, deg=moments.shape[-1]-1).T
        return gt.linalg.lstsq_ec(polemat, funcvec, constrain_mat, moments)
    return np.linalg.lstsq(polemat, funcvec, rcond=None)[0]


def residues_hybr_ols_b(z, fct_z, tau, fct_tau, poles, beta, moments=(), weight=False, weight_ratio=[.5, .5]):
    """Calculate residues fitting Matsubara as well as imaginary time data."""
    polematrix_z = 1./np.subtract.outer(z, poles)
    polematrix_tau = gt.pole_gf_tau_b(tau[:, newaxis], weights=1, poles=poles[:, newaxis], beta=beta)
    polemat = np.concatenate((polematrix_z, polematrix_tau), axis=-2)
    funcvec = np.concatenate((fct_z, fct_tau), axis=-1)
    scaling = 1./np.linalg.norm(polemat, axis=-1, keepdims=True)
    scaling = np.ones_like(polemat)
    if np.any(weight):
        scaling *= weight[..., np.newaxis]
    polemat *= scaling
    funcvec *= scaling[..., 0]

    # weight fct_z/fct_tau according to weight_ratio:
    rows = polemat.shape[-2]
    polemat[:z.size] *= weight_ratio[0] * rows / z.size  # weight of z data
    funcvec[:z.size] *= weight_ratio[0] * rows / z.size  # weight of z data
    polemat[z.size:] *= weight_ratio[1] * rows / tau.size  # weight of tau data
    funcvec[z.size:] *= weight_ratio[1] * rows / tau.size  # weight of tau data
    if moments:  # FIXME: allow also other constrains, like occupation Number
        moments = np.array(moments)
        constrain_mat = np.polynomial.polynomial.polyvander(poles, deg=moments.shape[-1]-1).T
        return gt.linalg.lstsq_ec(polemat, funcvec, constrain_mat, moments)
    return np.linalg.lstsq(polemat, funcvec, rcond=None)[0]


def residues_tls(z, fct_z, poles, weight=None, constrains=None):
    polematrix = 1./np.subtract.outer(z, poles)
    if weight is not None:
        polematrix *= weight[..., np.newaxis]
        fct_z *= weight
    if constrains is not None:
        # TODO: add constrains
        raise NotImplementedError
    __, sigma, vh = np.linalg.svd(np.concatenate((polematrix, fct_z[..., np.newaxis]), axis=-1))
    print('TLS sigma: ', sigma)
    print(vh.shape, vh[-1, -1])
    return -vh[-1, :-1]/vh[-1, -1]


def residues_odr(z, fct_z, poles, weight=False):
    """Calculate the residues using orthogonal distance regression.

    This assumes that not only `fct_z` contains errors, but also `poles`.

    Parameters
    ----------
    weight : (N_z) float np.ndarray, optional
        Weighting of the data points, for a known error `σ` this should be
        `weight = 1./σ`.

    Returns
    -------
    residues : (M) complex np.ndarray
        The residues corresponding to the `poles`.

    """
    def odr_residues(residues_, pole_matrix):
        import ipdb; ipdb.set_trace()
        return np.sum(pole_matrix.T*residues_, axis=-1)[np.newaxis]
        return gt.pole_gf_z(z, poles=poles_, weights=residues_)

    regression = scipy.odr.ODR(
        data=scipy.odr.Data(x=1./(z - poles[:, np.newaxis]), y=fct_z[np.newaxis]),
        model=scipy.odr.Model(odr_residues),
        beta0=residues_ols(z, fct_z, poles=poles, weight=weight)[0],
    ).run()

    return regression


def asymtotic(z, fct_z, roots, poles, weight=False):
    """Calculate large `z` asymptotic from `roots` and `poles`.

    Parameters
    ----------
    z, fct_z : (N_z) complex np.ndarray
        Variable where function is evaluated and function values.
    poles : (M) complex np.ndarray
        Position of the poles of the function.
    roots : (N) complex np.ndarray
        Position of the roots of the function.
    weight : (N_z) float np.ndarray, optional
        Weighting of the data points, for a known error `σ` this should be
        `weight = 1./σ`.

    Returns
    -------
    asym, std : float
        Large `z` asymptotic and its standard deviation.

    """
    ratios = fct_z/np.prod(np.subtract.outer(z, roots), axis=-1) \
        * np.prod(np.subtract.outer(z, poles), axis=-1)
    if weight is False:
        asym = np.mean(ratios, axis=-1)
        std = np.std(ratios, ddof=1, axis=-1)
    else:
        asym = np.average(ratios, weights=weight, axis=-1)
        std = np.average(abs(ratios - asym)**2, weights=weight, axis=-1)
    return asym, std


def physical(z, fct_z, poles0, weights0, weight):
    num = 10000  # mesh points on which positivity is checked
    # starting from a good guess, fit the poles

    def pole_gf(z_, *params):
        z_ = z_.view(complex)
        params = np.array(params).view(complex)
        weights = params[:weights0.size]
        poles = params[weights0.size:]
        # check for 10 halfwidths
        lower = min(poles0.real + 10*abs(poles.imag))
        upper = max(poles0.real + 10*abs(poles.imag))
        relevant = np.linspace(lower, upper, num=num)
        check = gt.pole_gf_z(relevant, poles, weights=weights).imag
        check[check < 0] = 0
        return np.concatenate((gt.pole_gf_z(z_, poles, weights=weights).view(float), check))

    # import ipdb; ipdb.set_trace()
    pole_bounds_upper = np.empty_like(poles0)
    pole_bounds_upper.real = np.infty
    pole_bounds_upper.imag = 0
    pole_bounds_lower = np.empty_like(poles0)
    pole_bounds_lower.real = -np.infty
    pole_bounds_lower.imag = -np.infty
    weight_bounds_upper = np.empty_like(weights0)
    weight_bounds_upper.real = np.infty
    weight_bounds_upper.imag = np.infty
    weight_bounds_lower = np.empty_like(weights0)
    weight_bounds_lower.real = -np.infty
    weight_bounds_lower.imag = -np.infty

    # if weights0[np.argmax(poles0.real)] < 0:
    #     print('WARNING rightmost pole has negative residue!!')
    # else:
    #     weight_bounds_lower[np.argmax(weights0.real)] = 0
    # if weights0[np.argmin(poles0.real)] < 0:
    #     print('WARNING leftmost pole has negative residue!!')
    # else:
    #     weight_bounds_lower[np.argmin(weights0.real)] = 0

    if weight is not None:
        sigma = 1./(weight if np.iscomplexobj(weight) else weight + 1j*weight).view(float)
        sigma = np.concatenate((sigma, np.full(num, sigma.min())))
    else:
        sigma = None

    weights0[weights0 < 0] = 0

    fit, __ = spopt.curve_fit(
        pole_gf, xdata=z.view(float), ydata=np.concatenate((fct_z.view(float), np.zeros(num))),
        p0=np.concatenate((weights0.view(float), poles0.view(float))),
        bounds=(np.concatenate((weight_bounds_lower.view(float), pole_bounds_lower.view(float))),
                np.concatenate((weight_bounds_upper.view(float), pole_bounds_upper.view(float)))),
        sigma=sigma,
    )
    fit = np.array(fit).view(complex)
    weights = fit[:weights0.size]
    poles = fit[weights0.size:]
    initial_residue = abs(fct_z - pole_gf(z, *weights0.view(float), *poles0.view(float)).view(complex)[:fct_z.size])
    final_residue = abs(fct_z - pole_gf(z, *weights.view(float), *poles.view(float)).view(complex)[:fct_z.size])
    print('init ', initial_residue)
    print('final', final_residue)
    return poles, weights


def physical_strict(z, fct_z, poles0, weights0, weight):
    # starting from a good guess, fit the poles
    def pole_gf(z_, *params):
        z_ = z_.view(complex)
        weights = np.array(params[:weights0.size])
        poles = np.array(params[weights0.size:]).view(complex)
        return gt.pole_gf_z(z_, poles, weights=weights).view(float)

    # import ipdb; ipdb.set_trace()
    pole_bounds_upper = np.empty_like(poles0)
    pole_bounds_upper.real = np.infty
    pole_bounds_upper.imag = 0
    pole_bounds_lower = np.empty_like(poles0)
    pole_bounds_lower.real = -np.infty
    pole_bounds_lower.imag = -np.infty
    weigt_bounds_upper = np.full_like(weights0.real, +np.infty)
    weigt_bounds_lower = np.full_like(weights0.real, 0)

    if weight is not None:
        sigma = 1./(weight if np.iscomplexobj(weight) else weight + 1j*weight).view(float)
    else:
        sigma = None

    weights0[weights0 < 0] = 0

    fit, __ = spopt.curve_fit(
        pole_gf, xdata=z.view(float), ydata=fct_z.view(float),
        p0=np.concatenate((weights0.real, poles0.view(float))),
        bounds=(np.concatenate((weigt_bounds_lower, pole_bounds_lower.view(float))),
                np.concatenate((weigt_bounds_upper, pole_bounds_upper.view(float)))),
        sigma=sigma,
    )
    weights = fit[:weights0.size]
    poles = fit[weights.size:].view(complex)
    initial_residue = abs(fct_z - pole_gf(z, *weights0.real, *poles0.view(float)).view(complex))
    final_residue = abs(fct_z - pole_gf(z, *weights.real, *poles.view(float)).view(complex))
    print('init ', initial_residue)
    print('final', final_residue)
    return poles, weights
