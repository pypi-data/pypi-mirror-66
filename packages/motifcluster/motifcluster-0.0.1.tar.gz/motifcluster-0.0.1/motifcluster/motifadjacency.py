"""
Functions for building motif adjacency matrices
are in `motifcluster.motifadjacency`.
"""

from scipy import sparse

from motifcluster import utils as mcut
from motifcluster import indicators as mcin

def build_motif_adjacency_matrix(adj_mat, motif_name, motif_type = "struc",
  mam_weight_type = "unweighted", mam_method = "sparse"):

  """
  Build a motif adjacency matrix.

  Build a motif adjacency matrix from an adjacency matrix.
  Entry (`i, j`) of a motif adjacency matrix is the
  sum of the weights of all motifs containing both
  nodes `i` and `j`.

  - The motif is specified by name and the type of motif instance can be one of:

    - Functional: motifs should appear as subgraphs.
    - Structural: motifs should appear as induced subgraphs.

  - The weighting scheme can be one of:

    - Unweighted: the weight of any motif instance is one.
    - Mean: the weight of any motif instance
      is the mean of its edge weights.
    - Product: the weight of any motif instance
      is the product of its edge weights.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  motif_name : str
    Motif used for the motif adjacency matrix.
  motif_type : str
    Type of motif adjacency matrix to build.
    One of `"func"` or `"struc"`.
  mam_weight_type : str
    The weighting scheme to use.
    One of `"unweighted"`, `"mean"` or `"product"`.
  mam_method : str
    Which formulation to use.
    One of `"dense"` or `"sparse"`.
    The sparse formulation avoids generating large dense matrices
    so tends to be faster for large sparse graphs.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.

  Examples
  --------
  >>> adj_mat = np.array(range(1, 10)).reshape((3, 3))
  >>> build_motif_adjacency_matrix(adj_mat, "M1", "func", "mean")
  """

  # check args
  assert motif_name in mcut.get_motif_names()
  assert motif_type in ["struc", "func"]
  assert mam_weight_type in ["unweighted", "mean", "product"]
  assert mam_method in ["sparse", "dense"]

  adj_mat = sparse.csr_matrix(adj_mat)

  if motif_name == "Ms":
    return mam_Ms(adj_mat, motif_type, mam_weight_type)

  elif motif_name == "Md":
    return mam_Md(adj_mat, mam_weight_type)

  elif motif_name == "M1":
    return mam_M1(adj_mat, motif_type, mam_weight_type)

  elif motif_name == "M2":
    return mam_M2(adj_mat, motif_type, mam_weight_type)

  elif motif_name == "M3":
    return mam_M3(adj_mat, motif_type, mam_weight_type)

  elif motif_name == "M4":
    return mam_M4(adj_mat, mam_weight_type)

  elif motif_name == "M5":
    return mam_M5(adj_mat, motif_type, mam_weight_type)

  elif motif_name == "M6":
    return mam_M6(adj_mat, motif_type, mam_weight_type)

  elif motif_name == "M7":
    return mam_M7(adj_mat, motif_type, mam_weight_type)

  elif motif_name == "M8":
    return mam_M8(adj_mat, motif_type, mam_weight_type, mam_method)

  elif motif_name == "M9":
    return mam_M9(adj_mat, motif_type, mam_weight_type, mam_method)

  elif motif_name == "M10":
    return mam_M10(adj_mat, motif_type, mam_weight_type, mam_method)

  elif motif_name == "M11":
    return mam_M11(adj_mat, motif_type, mam_weight_type, mam_method)

  elif motif_name == "M12":
    return mam_M12(adj_mat, motif_type, mam_weight_type, mam_method)

  elif motif_name == "M13":
    return mam_M13(adj_mat, motif_type, mam_weight_type, mam_method)

  elif motif_name == "Mcoll":
    return mam_Mcoll(adj_mat, motif_type, mam_weight_type, mam_method)

  elif motif_name == "Mexpa":
    return mam_Mexpa(adj_mat, motif_type, mam_weight_type, mam_method)


def mam_Ms(adj_mat, motif_type, mam_weight_type):

  """
  Perform the motif adjacency matrix calculations for motif Ms.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  motif_type : str
    Type of motif adjacency matrix to build.
  mam_weight_type : str
    The weighting scheme to use. One of `"unweighted"`, `"mean"` or `"product"`.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.
  """

  if mam_weight_type == "unweighted":
    if motif_type == "func":
      J = mcin._build_J(adj_mat)
      return J + J.transpose()

    if motif_type == "struc":
      Js = mcin._build_Js(adj_mat)
      return Js + Js.transpose()

  if mam_weight_type == "mean":
    if motif_type == "func":
      G = mcin._build_G(adj_mat)
      return G + G.transpose()

    if motif_type == "struc":
      Gs = mcin._build_Gs(adj_mat)
      return Gs + Gs.transpose()

  if mam_weight_type == "product":
    if motif_type == "func":
      G = mcin._build_G(adj_mat)
      return G + G.transpose()

    if motif_type == "struc":
      Gs = mcin._build_Gs(adj_mat)
      return Gs + Gs.transpose()


def mam_Md(adj_mat, mam_weight_type):

  """
  Perform the motif adjacency matrix calculations for motif Md.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  mam_weight_type : str
    The weighting scheme to use. One of `"unweighted"`, `"mean"` or `"product"`.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.
  """

  if mam_weight_type == "unweighted":
    Jd = mcin._build_Jd(adj_mat)
    return Jd

  if mam_weight_type == "mean":
    Gd = mcin._build_Gd(adj_mat)
    return Gd / 2

  if mam_weight_type == "product":
    Gp = mcin._build_Gp(adj_mat)
    return Gp


def mam_M1(adj_mat, motif_type, mam_weight_type):

  """
  Perform the motif adjacency matrix calculations for motif M1.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  motif_type : str
    Type of motif adjacency matrix to build.
  mam_weight_type : str
    The weighting scheme to use. One of `"unweighted"`, `"mean"` or `"product"`.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.
  """

  if mam_weight_type == "unweighted":
    if motif_type == "func":
      J = mcin._build_J(adj_mat)
      C = J.transpose().multiply(J * J)
      return C + C.transpose()

    if motif_type == "struc":
      Js = mcin._build_Js(adj_mat)
      C = Js.transpose().multiply(Js * Js)
      return C + C.transpose()

  if mam_weight_type == "mean":
    if motif_type == "func":
      J = mcin._build_J(adj_mat)
      G = mcin._build_G(adj_mat)
      C = J.transpose().multiply(J * G) + J.transpose().multiply(G * J) + G.transpose().multiply(J * J)
      return (C + C.transpose()) / 3

    if motif_type == "struc":
      Js = mcin._build_Js(adj_mat)
      Gs = mcin._build_Gs(adj_mat)
      C = Js.transpose().multiply(Js * Gs) + Js.transpose().multiply(Gs * Js) + Gs.transpose().multiply(Js * Js)
      return (C + C.transpose()) / 3

  if mam_weight_type == "product":
    if motif_type == "func":
      G = mcin._build_G(adj_mat)
      C = G.transpose().multiply(G * G)
      return C + C.transpose()

    if motif_type == "struc":
      Gs = mcin._build_Gs(adj_mat)
      C = Gs.transpose().multiply(Gs * Gs)
      return C + C.transpose()


def mam_M2(adj_mat, motif_type, mam_weight_type):

  """
  Perform the motif adjacency matrix calculations for motif M2.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  motif_type : str
    Type of motif adjacency matrix to build.
  mam_weight_type : str
    The weighting scheme to use. One of `"unweighted"`, `"mean"` or `"product"`.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.
  """

  if mam_weight_type == "unweighted":
    if motif_type == "func":
      J = mcin._build_J(adj_mat)
      Jd = mcin._build_Jd(adj_mat)
      C = J.transpose().multiply(Jd * J) + J.transpose().multiply(J * Jd) + Jd.multiply(J * J)
      return C + C.transpose()

    if motif_type == "struc":
      Js = mcin._build_Js(adj_mat)
      Jd = mcin._build_Jd(adj_mat)
      C = Js.transpose().multiply(Jd * Js) + Js.transpose().multiply(Js * Jd) + Jd.multiply(Js * Js)
      return C + C.transpose()

  if mam_weight_type == "mean":
    if motif_type == "func":
      J = mcin._build_J(adj_mat)
      Jd = mcin._build_Jd(adj_mat)
      Gd = mcin._build_Gd(adj_mat)
      G = mcin._build_G(adj_mat)
      C = J.transpose().multiply(Jd * G) + J.transpose().multiply(Gd * J) + G.transpose().multiply(Jd * J)
      C = C + J.transpose().multiply(J * Gd) + J.transpose().multiply(G * Jd) + G.transpose().multiply(J * Jd)
      C = C + Jd.multiply(J * G) + Jd.multiply(G * J) + Gd.multiply(J * J)
      return (C + C.transpose()) / 4

    if motif_type == "struc":
      Js = mcin._build_Js(adj_mat)
      Jd = mcin._build_Jd(adj_mat)
      Gs = mcin._build_Gs(adj_mat)
      Gd = mcin._build_Gd(adj_mat)
      C = Js.transpose().multiply(Jd * Gs) + Js.transpose().multiply(Gd * Js) + Gs.transpose().multiply(Jd * Js)
      C = C + Js.transpose().multiply(Js * Gd) + Js.transpose().multiply(Gs * Jd) + Gs.transpose().multiply(Js * Jd)
      C = C + Jd.multiply(Js * Gs) + Jd.multiply(Gs * Js) + Gd.multiply(Js * Js)
      return (C + C.transpose()) / 4

  if mam_weight_type == "product":
    if motif_type == "func":
      G = mcin._build_G(adj_mat)
      Gp = mcin._build_Gp(adj_mat)
      C = G.transpose().multiply(Gp * G) + G.transpose().multiply(G * Gp) + Gp.multiply(G * G)
      return C + C.transpose()

    if motif_type == "struc":
      Gs = mcin._build_Gs(adj_mat)
      Gp = mcin._build_Gp(adj_mat)
      C = Gs.transpose().multiply(Gp * Gs) + Gs.transpose().multiply(Gs * Gp) + Gp.multiply(Gs * Gs)
      return C + C.transpose()


def mam_M3(adj_mat, motif_type, mam_weight_type):

  """
  Perform the motif adjacency matrix calculations for motif M3.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  motif_type : str
    Type of motif adjacency matrix to build.
  mam_weight_type : str
    The weighting scheme to use. One of `"unweighted"`, `"mean"` or `"product"`.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.
  """

  if mam_weight_type == "unweighted":
    if motif_type == "func":
      J = mcin._build_J(adj_mat)
      Jd = mcin._build_Jd(adj_mat)
      C = J.multiply(Jd * Jd) + Jd.multiply(Jd * J) + Jd.multiply(J * Jd)
      return C + C.transpose()

    if motif_type == "struc":
      Js = mcin._build_Js(adj_mat)
      Jd = mcin._build_Jd(adj_mat)
      C = Js.multiply(Jd * Jd) + Jd.multiply(Jd * Js) + Jd.multiply(Js * Jd)
      return C + C.transpose()

  if mam_weight_type == "mean":
    if motif_type == "func":
      J = mcin._build_J(adj_mat)
      Jd = mcin._build_Jd(adj_mat)
      Gd = mcin._build_Gd(adj_mat)
      G = mcin._build_G(adj_mat)
      C = J.multiply(Jd * Gd) + J.multiply(Gd * Jd) + G.multiply(Jd * Jd)
      C = C + Jd.multiply(Jd * G) + Jd.multiply(Gd * J) + Gd.multiply(Jd * J)
      C = C + Jd.multiply(J * Gd) + Jd.multiply(G * Jd) + Gd.multiply(J * Jd)
      return (C + C.transpose()) / 5

    if motif_type == "struc":
      Js = mcin._build_Js(adj_mat)
      Jd = mcin._build_Jd(adj_mat)
      Gs = mcin._build_Gs(adj_mat)
      Gd = mcin._build_Gd(adj_mat)
      C = Js.multiply(Jd * Gd) + Js.multiply(Gd * Jd) + Gs.multiply(Jd * Jd)
      C = C + Jd.multiply(Jd * Gs) + Jd.multiply(Gd * Js) + Gd.multiply(Jd * Js)
      C = C + Jd.multiply(Js * Gd) + Jd.multiply(Gs * Jd) + Gd.multiply(Js * Jd)
      return (C + C.transpose()) / 5

  if mam_weight_type == "product":
    if motif_type == "func":
      G = mcin._build_G(adj_mat)
      Gp = mcin._build_Gp(adj_mat)
      C = G.multiply(Gp * Gp) + Gp.multiply(Gp * G) + Gp.multiply(G * Gp)
      return C + C.transpose()

    if motif_type == "struc":
      Gs = mcin._build_Gs(adj_mat)
      Gp = mcin._build_Gp(adj_mat)
      C = Gs.multiply(Gp * Gp) + Gp.multiply(Gp * Gs) + Gp.multiply(Gs * Gp)
      return C + C.transpose()


def mam_M4(adj_mat, mam_weight_type):

  """
  Perform the motif adjacency matrix calculations for motif M4.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  mam_weight_type : str
    The weighting scheme to use. One of `"unweighted"`, `"mean"` or `"product"`.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.
  """

  if mam_weight_type == "unweighted":
    Jd = mcin._build_Jd(adj_mat)
    return Jd.multiply(Jd * Jd)

  if mam_weight_type == "mean":
    Jd = mcin._build_Jd(adj_mat)
    Gd = mcin._build_Gd(adj_mat)
    return (Jd.multiply(Jd * Gd) + Jd.multiply(Gd * Jd) + Gd.multiply(Jd * Jd)) / 6

  if mam_weight_type == "product":
    Gp = mcin._build_Gp(adj_mat)
    return Gp.multiply(Gp * Gp)


def mam_M5(adj_mat, motif_type, mam_weight_type):

  """
  Perform the motif adjacency matrix calculations for motif M5.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  motif_type : str
    Type of motif adjacency matrix to build.
  mam_weight_type : str
    The weighting scheme to use. One of `"unweighted"`, `"mean"` or `"product"`.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.
  """

  if mam_weight_type == "unweighted":
    if motif_type == "func":
      J = mcin._build_J(adj_mat)
      C = J.multiply(J * J) + J.multiply(J * J.transpose()) + J.multiply(J.transpose() * J)
      return C + C.transpose()

    if motif_type == "struc":
      Js = mcin._build_Js(adj_mat)
      C = Js.multiply(Js * Js) + Js.multiply(Js * Js.transpose()) + Js.multiply(Js.transpose() * Js)
      return C + C.transpose()

  if mam_weight_type == "mean":
    if motif_type == "func":
      J = mcin._build_J(adj_mat)
      G = mcin._build_G(adj_mat)
      C = J.multiply(J * G) + J.multiply(G * J) + G.multiply(J * J)
      C = C + J.multiply(J * G.transpose()) + J.multiply(G * J.transpose()) + G.multiply(J * J.transpose())
      C = C + J.multiply(J.transpose() * G) + J.multiply(G.transpose() * J) + G.multiply(J.transpose() * J)
      return (C + C.transpose()) / 3

    if motif_type == "struc":
      Js = mcin._build_Js(adj_mat)
      Gs = mcin._build_Gs(adj_mat)
      C = Js.multiply(Js * Gs) + Js.multiply(Gs * Js) + Gs.multiply(Js * Js)
      C = C + Js.multiply(Js * Gs.transpose()) + Js.multiply(Gs * Js.transpose()) + Gs.multiply(Js * Js.transpose())
      C = C + Js.multiply(Js.transpose() * Gs) + Js.multiply(Gs.transpose() * Js) + Gs.multiply(Js.transpose() * Js)
      return (C + C.transpose()) / 3

  if mam_weight_type == "product":
    if motif_type == "func":
      G = mcin._build_G(adj_mat)
      C = G.multiply(G * G) + G.multiply(G * G.transpose()) + G.multiply(G.transpose() * G)
      return C + C.transpose()

    if motif_type == "struc":
      Gs = mcin._build_Gs(adj_mat)
      C = Gs.multiply(Gs * Gs) + Gs.multiply(Gs * Gs.transpose()) + Gs.multiply(Gs.transpose() * Gs)
      return C + C.transpose()


def mam_M6(adj_mat, motif_type, mam_weight_type):

  """
  Perform the motif adjacency matrix calculations for motif M6.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  motif_type : str
    Type of motif adjacency matrix to build.
  mam_weight_type : str
    The weighting scheme to use. One of `"unweighted"`, `"mean"` or `"product"`.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.
  """

  if mam_weight_type == "unweighted":
    if motif_type == "func":
      J = mcin._build_J(adj_mat)
      Jd = mcin._build_Jd(adj_mat)
      C = J.multiply(J * Jd)
      Cprime = Jd.multiply(J.transpose() * J)
      return C + C.transpose() + Cprime

    if motif_type == "struc":
      Js = mcin._build_Js(adj_mat)
      Jd = mcin._build_Jd(adj_mat)
      C = Js.multiply(Js * Jd)
      Cprime = Jd.multiply(Js.transpose() * Js)
      return C + C.transpose() + Cprime

  if mam_weight_type == "mean":
    if motif_type == "func":
      J = mcin._build_J(adj_mat)
      Jd = mcin._build_Jd(adj_mat)
      Gd = mcin._build_Gd(adj_mat)
      G = mcin._build_G(adj_mat)
      C = J.multiply(J * Gd) + J.multiply(G * Jd) + G.multiply(J * Jd)
      Cprime = Jd.multiply(J.transpose() * G) + Jd.multiply(G.transpose() * J) + Gd.multiply(J.transpose() * J)
      return (C + C.transpose() + Cprime) / 4

    if motif_type == "struc":
      Js = mcin._build_Js(adj_mat)
      Gs = mcin._build_Gs(adj_mat)
      Jd = mcin._build_Jd(adj_mat)
      Gd = mcin._build_Gd(adj_mat)
      C = Js.multiply(Js * Gd) + Js.multiply(Gs * Jd) + Gs.multiply(Js * Jd)
      Cprime = Jd.multiply(Js.transpose() * Gs) + Jd.multiply(Gs.transpose() * Js) + Gd.multiply(Js.transpose() * Js)
      return (C + C.transpose() + Cprime) / 4

  if mam_weight_type == "product":
    if motif_type == "func":
      G = mcin._build_G(adj_mat)
      Gp = mcin._build_Gp(adj_mat)
      C = G.multiply(G * Gp)
      Cprime = Gp.multiply(G.transpose() * G)
      return C + C.transpose() + Cprime

    if motif_type == "struc":
      Gs = mcin._build_Gs(adj_mat)
      Gp = mcin._build_Gp(adj_mat)
      C = Gs.multiply(Gs * Gp)
      Cprime = Gp.multiply(Gs.transpose() * Gs)
      return C + C.transpose() + Cprime


def mam_M7(adj_mat, motif_type, mam_weight_type):

  """
  Perform the motif adjacency matrix calculations for motif M7.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  motif_type : str
    Type of motif adjacency matrix to build.
  mam_weight_type : str
    The weighting scheme to use. One of `"unweighted"`, `"mean"` or `"product"`.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.
  """

  if mam_weight_type == "unweighted":
    if motif_type == "func":
      J = mcin._build_J(adj_mat)
      Jd = mcin._build_Jd(adj_mat)
      C = J.multiply(Jd * J)
      Cprime = Jd.multiply(J * J.transpose())
      return C + C.transpose() + Cprime

    if motif_type == "struc":
      Js = mcin._build_Js(adj_mat)
      Jd = mcin._build_Jd(adj_mat)
      C = Js.multiply(Jd * Js)
      Cprime = Jd.multiply(Js * Js.transpose())
      return C + C.transpose() + Cprime

  if mam_weight_type == "mean":
    if motif_type == "func":
      J = mcin._build_J(adj_mat)
      Jd = mcin._build_Jd(adj_mat)
      Gd = mcin._build_Gd(adj_mat)
      G = mcin._build_G(adj_mat)
      C = J.multiply(Jd * G) + J.multiply(Gd * J) + G.multiply(Jd * J)
      Cprime = Jd.multiply(J * G.transpose()) + Jd.multiply(G * J.transpose()) + Gd.multiply(J * J.transpose())
      return (C + C.transpose() + Cprime) / 4

    if motif_type == "struc":
      Js = mcin._build_Js(adj_mat)
      Gs = mcin._build_Gs(adj_mat)
      Jd = mcin._build_Jd(adj_mat)
      Gd = mcin._build_Gd(adj_mat)
      C = Js.multiply(Jd * Gs) + Js.multiply(Gd * Js) + Gs.multiply(Jd * Js)
      Cprime = Jd.multiply(Js * Gs.transpose()) + Jd.multiply(Gs * Js.transpose()) + Gd.multiply(Js * Js.transpose())
      return (C + C.transpose() + Cprime) / 4

  if mam_weight_type == "product":
    if motif_type == "func":
      G = mcin._build_G(adj_mat)
      Gp = mcin._build_Gp(adj_mat)
      C = G.multiply(Gp * G)
      Cprime = Gp.multiply(G * G.transpose())
      return C + C.transpose() + Cprime

    if motif_type == "struc":
      Gs = mcin._build_Gs(adj_mat)
      Gp = mcin._build_Gp(adj_mat)
      C = Gs.multiply(Gp * Gs)
      Cprime = Gp.multiply(Gs * Gs.transpose())
      return C + C.transpose() + Cprime


def mam_M8(adj_mat, motif_type, mam_weight_type, mam_method):

  """
  Perform the motif adjacency matrix calculations for motif M8.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  motif_type : str
    Type of motif adjacency matrix to build.
  mam_weight_type : str
    The weighting scheme to use. One of `"unweighted"`, `"mean"` or `"product"`.
  mam_method : str
    Which formulation to use. One of `"dense"` or `"sparse"`.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.
  """

  if mam_method == "dense":
    if mam_weight_type == "unweighted":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        C = J.multiply(J * Jn)
        Cprime = Jn.multiply(J.transpose() * J)
        return C + C.transpose() + Cprime

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        C = Js.multiply(Js * J0)
        Cprime = J0.multiply(Js.transpose() * Js)
        return C + C.transpose() + Cprime

    if mam_weight_type == "mean":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        G = mcin._build_G(adj_mat)
        C = J.multiply(G * Jn) + G.multiply(J * Jn)
        Cprime = Jn.multiply(J.transpose() * G) + Jn.multiply(G.transpose() * J)
        return (C + C.transpose() + Cprime) / 2

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        C = Js.multiply(Gs * J0) + Gs.multiply(Js * J0)
        Cprime = J0.multiply(Js.transpose() * Gs) + J0.multiply(Gs.transpose() * Js)
        return (C + C.transpose() + Cprime) / 2

    if mam_weight_type == "product":
      if motif_type == "func":
        G = mcin._build_G(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        C = G.multiply(G * Jn)
        Cprime = Jn.multiply(G.transpose() * G)
        return C + C.transpose() + Cprime

      if motif_type == "struc":
        Gs = mcin._build_Gs(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        C = Gs.multiply(Gs * J0)
        Cprime = J0.multiply(Gs.transpose() * Gs)
        return C + C.transpose() + Cprime

  if mam_method == "sparse":
    if mam_weight_type == "unweighted":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = mcut._a_b_one(J, J) - J.multiply(J)
        Cprime = J.transpose() * J - Id.multiply(J.transpose() * J)
        return sparse.csr_matrix(C + C.transpose() + Cprime)

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = mcut._a_b_one(Js, Js) - Js.multiply(Js * Je)
        Cprime = Js.transpose() * Js - Je.multiply(Js.transpose() * Js)
        return sparse.csr_matrix(C + C.transpose() + Cprime)

    if mam_weight_type == "mean":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        G = mcin._build_G(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = mcut._a_b_one(J, G) - J.multiply(G) + mcut._a_b_one(G, J) - G.multiply(J)
        Cprime = J.transpose() * G - Id.multiply(J.transpose() * G)
        Cprime = Cprime + G.transpose() * J - Id.multiply(G.transpose() * J)
        return sparse.csr_matrix(C + C.transpose() + Cprime) / 2

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = mcut._a_b_one(Js, Gs) - Js.multiply(Gs * Je)
        C = C + mcut._a_b_one(Gs, Js) - Gs.multiply(Js * Je)
        Cprime = Js.transpose() * Gs - Je.multiply(Js.transpose() * Gs)
        Cprime = Cprime + Gs.transpose() * Js - Je.multiply(Gs.transpose() * Js)
        return sparse.csr_matrix(C + C.transpose() + Cprime) / 2

    if mam_weight_type == "product":
      if motif_type == "func":
        G = mcin._build_G(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = mcut._a_b_one(G, G) - G.multiply(G)
        Cprime = G.transpose() * G - Id.multiply(G.transpose() * G)
        return sparse.csr_matrix(C + C.transpose() + Cprime)

      if motif_type == "struc":
        Gs = mcin._build_Gs(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = mcut._a_b_one(Gs, Gs) - Gs.multiply(Gs * Je)
        Cprime = Gs.transpose() * Gs - Je.multiply(Gs.transpose() * Gs)
        return sparse.csr_matrix(C + C.transpose() + Cprime)


def mam_M9(adj_mat, motif_type, mam_weight_type, mam_method):

  """
  Perform the motif adjacency matrix calculations for motif M9.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  motif_type : str
    Type of motif adjacency matrix to build.
  mam_weight_type : str
    The weighting scheme to use. One of `"unweighted"`, `"mean"` or `"product"`.
  mam_method : str
    Which formulation to use. One of `"dense"` or `"sparse"`.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.
  """

  if mam_method == "dense":
    if mam_weight_type == "unweighted":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        C = J.multiply(Jn * J.transpose()) + Jn.multiply(J * J) + J.multiply(J.transpose() * Jn)
        return C + C.transpose()

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        C = Js.multiply(J0 * Js.transpose()) + J0.multiply(Js * Js) + Js.multiply(Js.transpose() * J0)
        return C + C.transpose()

    if mam_weight_type == "mean":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        G = mcin._build_G(adj_mat)
        C = J.multiply(Jn * G.transpose()) + G.multiply(Jn * J.transpose())
        C = C + Jn.multiply(J * G) + Jn.multiply(G * J)
        C = C + J.multiply(G.transpose() * Jn) + G.multiply(J.transpose() * Jn)
        return (C + C.transpose()) / 2

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        C = Js.multiply(J0 * Gs.transpose()) + Gs.multiply(J0 * Js.transpose())
        C = C + J0.multiply(Js * Gs) + J0.multiply(Gs * Js)
        C = C + Js.multiply(Gs.transpose() * J0) + Gs.multiply(Js.transpose() * J0)
        return (C + C.transpose()) / 2

    if mam_weight_type == "product":
      if motif_type == "func":
        G = mcin._build_G(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        C = G.multiply(Jn * G.transpose()) + Jn.multiply(G * G) + G.multiply(G.transpose() * Jn)
        return C + C.transpose()

      if motif_type == "struc":
        Gs = mcin._build_Gs(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        C = Gs.multiply(J0 * Gs.transpose()) + J0.multiply(Gs * Gs) + Gs.multiply(Gs.transpose() * J0)
        return C + C.transpose()

  if mam_method == "sparse":
    if mam_weight_type == "unweighted":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = mcut._a_one_b(J, J.transpose()) - 2 * J.multiply(J.transpose()) + J * J
        C = C - Id.multiply(J * J) + mcut._a_b_one(J, J.transpose())
        return sparse.csr_matrix(C + C.transpose())

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = mcut._a_one_b(Js, Js.transpose()) - Js.multiply(Je * Js.transpose())
        C = C + Js * Js - Je.multiply(Js * Js)
        C = C + mcut._a_b_one(Js, Js.transpose()) - Js.multiply(Js.transpose() * Je)
        return sparse.csr_matrix(C + C.transpose())

    if mam_weight_type == "mean":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        G = mcin._build_G(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = mcut._a_one_b(J, G.transpose()) - 2 * J.multiply(G.transpose()) + J * G
        C = C + mcut._a_one_b(G, J.transpose()) - 2 * G.multiply(J.transpose()) + G * J
        C = C - Id.multiply(J * G) + mcut._a_b_one(J, G.transpose())
        C = C - Id.multiply(G * J) + mcut._a_b_one(G, J.transpose())
        return sparse.csr_matrix(C + C.transpose()) / 2

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = mcut._a_one_b(Js, Gs.transpose()) - Js.multiply(Je * Gs.transpose())
        C = C + mcut._a_one_b(Gs, Js.transpose()) - Gs.multiply(Je * Js.transpose())
        C = C + Js * Gs - Je.multiply(Js * Gs)
        C = C + mcut._a_b_one(Js, Gs.transpose()) - Js.multiply(Gs.transpose() * Je)
        C = C + Gs * Js - Je.multiply(Gs * Js)
        C = C + mcut._a_b_one(Gs, Js.transpose()) - Gs.multiply(Js.transpose() * Je)
        return sparse.csr_matrix(C + C.transpose()) / 2

    if mam_weight_type == "product":
      if motif_type == "func":
        G = mcin._build_G(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = mcut._a_one_b(G, G.transpose()) - 2 * G.multiply(G.transpose()) + G * G
        C = C - Id.multiply(G * G) + mcut._a_b_one(G, G.transpose())
        return sparse.csr_matrix(C + C.transpose())

      if motif_type == "struc":
        Gs = mcin._build_Gs(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = mcut._a_one_b(Gs, Gs.transpose()) - Gs.multiply(Je * Gs.transpose())
        C = C + Gs * Gs - Je.multiply(Gs * Gs)
        C = C + mcut._a_b_one(Gs, Gs.transpose()) - Gs.multiply(Gs.transpose() * Je)
        return sparse.csr_matrix(C + C.transpose())


def mam_M10(adj_mat, motif_type, mam_weight_type, mam_method):

  """
  Perform the motif adjacency matrix calculations for motif M10.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  motif_type : str
    Type of motif adjacency matrix to build.
  mam_weight_type : str
    The weighting scheme to use. One of `"unweighted"`, `"mean"` or `"product"`.
  mam_method : str
    Which formulation to use. One of `"dense"` or `"sparse"`.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.
  """

  if mam_method == "dense":
    if mam_weight_type == "unweighted":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        C = J.multiply(Jn * J)
        Cprime = Jn.multiply(J * J.transpose())
        return C + C.transpose() + Cprime

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        C = Js.multiply(J0 * Js)
        Cprime = J0.multiply(Js * Js.transpose())
        return C + C.transpose() + Cprime

    if mam_weight_type == "mean":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        G = mcin._build_G(adj_mat)
        C = J.multiply(Jn * G) + G.multiply(Jn * J)
        Cprime = Jn.multiply(J * G.transpose()) + Jn.multiply(G * J.transpose())
        return (C + C.transpose() + Cprime) / 2

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        C = Js.multiply(J0 * Gs) + Gs.multiply(J0 * Js)
        Cprime = J0.multiply(Js * Gs.transpose()) + J0.multiply(Gs * Js.transpose())
        return (C + C.transpose() + Cprime) / 2

    if mam_weight_type == "product":
      if motif_type == "func":
        G = mcin._build_G(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        C = G.multiply(Jn * G)
        Cprime = Jn.multiply(G * G.transpose())
        return C + C.transpose() + Cprime

      if motif_type == "struc":
        Gs = mcin._build_Gs(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        C = Gs.multiply(J0 * Gs)
        Cprime = J0.multiply(Gs * Gs.transpose())
        return C + C.transpose() + Cprime

  if mam_method == "sparse":
    if mam_weight_type == "unweighted":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = mcut._a_one_b(J, J) - J.multiply(J)
        Cprime = J * J.transpose() - Id.multiply(J * J.transpose())
        return sparse.csr_matrix(C + C.transpose() + Cprime)

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = mcut._a_one_b(Js, Js) - Js.multiply(Je * Js)
        Cprime = Js * Js.transpose() - Je.multiply(Js * Js.transpose())
        return sparse.csr_matrix(C + C.transpose() + Cprime)

    if mam_weight_type == "mean":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        G = mcin._build_G(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = mcut._a_one_b(J, G) - J.multiply(G) + mcut._a_one_b(G, J) - G.multiply(J)
        Cprime = J * G.transpose() - Id.multiply(J * G.transpose())
        Cprime = Cprime + G * J.transpose() - Id.multiply(G * J.transpose())
        return sparse.csr_matrix(C + C.transpose() + Cprime) / 2

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = mcut._a_one_b(Js, Gs) - Js.multiply(Je * Gs)
        C = C + mcut._a_one_b(Gs, Js) - Gs.multiply(Je * Js)
        Cprime = Js * Gs.transpose() - Je.multiply(Js * Gs.transpose())
        Cprime = Cprime + Gs * Js.transpose() - Je.multiply(Gs * Js.transpose())
        return sparse.csr_matrix(C + C.transpose() + Cprime) / 2

    if mam_weight_type == "product":
      if motif_type == "func":
        G = mcin._build_G(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = mcut._a_one_b(G, G) - G.multiply(G)
        Cprime = G * G.transpose() - Id.multiply(G * G.transpose())
        return sparse.csr_matrix(C + C.transpose() + Cprime)

      if motif_type == "struc":
        Gs = mcin._build_Gs(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = mcut._a_one_b(Gs, Gs) - Gs.multiply(Je * Gs)
        Cprime = Gs * Gs.transpose() - Je.multiply(Gs * Gs.transpose())
        return sparse.csr_matrix(C + C.transpose() + Cprime)


def mam_M11(adj_mat, motif_type, mam_weight_type, mam_method):

  """
  Perform the motif adjacency matrix calculations for motif M11.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  motif_type : str
    Type of motif adjacency matrix to build.
  mam_weight_type : str
    The weighting scheme to use. One of `"unweighted"`, `"mean"` or `"product"`.
  mam_method : str
    Which formulation to use. One of `"dense"` or `"sparse"`.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.
  """

  if mam_method == "dense":
    if mam_weight_type == "unweighted":
      if motif_type == "func":
        Jd = mcin._build_Jd(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        J = mcin._build_J(adj_mat)
        C = Jd.multiply(J * Jn) + Jn.multiply(Jd * J) + J.multiply(Jd * Jn)
        return C + C.transpose()

      if motif_type == "struc":
        Jd = mcin._build_Jd(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        Js = mcin._build_Js(adj_mat)
        C = Jd.multiply(Js * J0) + J0.multiply(Jd * Js) + Js.multiply(Jd * J0)
        return C + C.transpose()

    if mam_weight_type == "mean":
      if motif_type == "func":
        Jd = mcin._build_Jd(adj_mat)
        Gd = mcin._build_Gd(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        J = mcin._build_J(adj_mat)
        G = mcin._build_G(adj_mat)
        C = Jd.multiply(G * Jn) + Gd.multiply(J * Jn)
        C = C + Jn.multiply(Jd * G) + Jn.multiply(Gd * J)
        C = C + J.multiply(Gd * Jn) + G.multiply(Jd * Jn)
        return (C + C.transpose()) / 3

      if motif_type == "struc":
        Jd = mcin._build_Jd(adj_mat)
        Gd = mcin._build_Gd(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        Js = mcin._build_Js(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        C = Jd.multiply(Gs * J0) + Gd.multiply(Js * J0)
        C = C + J0.multiply(Jd * Gs) + J0.multiply(Gd * Js)
        C = C + Js.multiply(Gd * J0) + Gs.multiply(Jd * J0)
        return (C + C.transpose()) / 3

    if mam_weight_type == "product":
      if motif_type == "func":
        Gp = mcin._build_Gp(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        G = mcin._build_G(adj_mat)
        C = Gp.multiply(G * Jn) + Jn.multiply(Gp * G) + G.multiply(Gp * Jn)
        return C + C.transpose()

      if motif_type == "struc":
        Gp = mcin._build_Gp(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        C = Gp.multiply(Gs * J0) + J0.multiply(Gp * Gs) + Gs.multiply(Gp * J0)
        return C + C.transpose()

  if mam_method == "sparse":
    if mam_weight_type == "unweighted":
      if motif_type == "func":
        Jd = mcin._build_Jd(adj_mat)
        Id = mcin._build_Id(adj_mat)
        J = mcin._build_J(adj_mat)
        C = mcut._a_b_one(Jd, J) - Jd.multiply(J)
        C = C + Jd * J - Id.multiply(Jd * J)
        C = C + mcut._a_b_one(J, Jd) - J.multiply(Jd)
        return sparse.csr_matrix(C + C.transpose())

      if motif_type == "struc":
        Jd = mcin._build_Jd(adj_mat)
        Je = mcin._build_Je(adj_mat)
        Js = mcin._build_Js(adj_mat)
        C = mcut._a_b_one(Jd, Js) - Jd.multiply(Js * Je)
        C = C + Jd * Js - Je.multiply(Jd * Js)
        C = C + mcut._a_b_one(Js, Jd) - Js.multiply(Jd * Je)
        return sparse.csr_matrix(C + C.transpose())

    if mam_weight_type == "mean":
      if motif_type == "func":
        Jd = mcin._build_Jd(adj_mat)
        Gd = mcin._build_Gd(adj_mat)
        Id = mcin._build_Id(adj_mat)
        J = mcin._build_J(adj_mat)
        G = mcin._build_G(adj_mat)
        C = mcut._a_b_one(Jd, G) - Jd.multiply(G) + mcut._a_b_one(Gd, J) - Gd.multiply(J)
        C = C + Jd * G - Id.multiply(Jd * G) + Gd * J - Id.multiply(Gd * J)
        C = C + mcut._a_b_one(J, Gd) - J.multiply(Gd) + mcut._a_b_one(G, Jd) - G.multiply(Jd)
        return sparse.csr_matrix(C + C.transpose()) / 3

      if motif_type == "struc":
        Jd = mcin._build_Jd(adj_mat)
        Gd = mcin._build_Gd(adj_mat)
        Je = mcin._build_Je(adj_mat)
        Js = mcin._build_Js(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        C = mcut._a_b_one(Jd, Gs) - Jd.multiply(Gs * Je)
        C = C + mcut._a_b_one(Gd, Js) - Gd.multiply(Js * Je)
        C = C + Jd * Gs - Je.multiply(Jd * Gs) + Gd * Js - Je.multiply(Gd * Js)
        C = C + mcut._a_b_one(Js, Gd) - Js.multiply(Gd * Je)
        C = C + mcut._a_b_one(Gs, Jd) - Gs.multiply(Jd * Je)
        return sparse.csr_matrix(C + C.transpose()) / 3

    if mam_weight_type == "product":
      if motif_type == "func":
        Gp = mcin._build_Gp(adj_mat)
        Id = mcin._build_Id(adj_mat)
        G = mcin._build_G(adj_mat)
        C = mcut._a_b_one(Gp, G) - Gp.multiply(G)
        C = C + Gp * G - Id.multiply(Gp * G)
        C = C + mcut._a_b_one(G, Gp) - G.multiply(Gp)
        return sparse.csr_matrix(C + C.transpose())

      if motif_type == "struc":
        Gp = mcin._build_Gp(adj_mat)
        Je = mcin._build_Je(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        C = mcut._a_b_one(Gp, Gs) - Gp.multiply(Gs * Je)
        C = C + Gp * Gs - Je.multiply(Gp * Gs)
        C = C + mcut._a_b_one(Gs, Gp) - Gs.multiply(Gp * Je)
        return sparse.csr_matrix(C + C.transpose())


def mam_M12(adj_mat, motif_type, mam_weight_type, mam_method):

  """
  Perform the motif adjacency matrix calculations for motif M12.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  motif_type : str
    Type of motif adjacency matrix to build.
  mam_weight_type : str
    The weighting scheme to use. One of `"unweighted"`, `"mean"` or `"product"`.
  mam_method : str
    Which formulation to use. One of `"dense"` or `"sparse"`.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.
  """

  if mam_method == "dense":
    if mam_weight_type == "unweighted":
      if motif_type == "func":
        Jd = mcin._build_Jd(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        J = mcin._build_J(adj_mat)
        C = Jd.multiply(Jn * J) + Jn.multiply(J * Jd) + J.multiply(Jn * Jd)
        return C + C.transpose()

      if motif_type == "struc":
        Jd = mcin._build_Jd(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        Js = mcin._build_Js(adj_mat)
        C = Jd.multiply(J0 * Js) + J0.multiply(Js * Jd) + Js.multiply(J0 * Jd)
        return C + C.transpose()

    if mam_weight_type == "mean":
      if motif_type == "func":
        Jd = mcin._build_Jd(adj_mat)
        Gd = mcin._build_Gd(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        G = mcin._build_G(adj_mat)
        J = mcin._build_J(adj_mat)
        C = Jd.multiply(Jn * G) + Gd.multiply(Jn * J)
        C = C + Jn.multiply(J * Gd) + Jn.multiply(G * Jd)
        C = C + J.multiply(Jn * Gd) + G.multiply(Jn * Jd)
        return (C + C.transpose()) / 3

      if motif_type == "struc":
        Jd = mcin._build_Jd(adj_mat)
        Gd = mcin._build_Gd(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        Js = mcin._build_Js(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        C = Jd.multiply(J0 * Gs) + Gd.multiply(J0 * Js)
        C = C + J0.multiply(Js * Gd) + J0.multiply(Gs * Jd)
        C = C + Js.multiply(J0 * Gd) + Gs.multiply(J0 * Jd)
        return (C + C.transpose()) / 3

    if mam_weight_type == "product":
      if motif_type == "func":
        Gp = mcin._build_Gp(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        G = mcin._build_G(adj_mat)
        C = Gp.multiply(Jn * G) + Jn.multiply(G * Gp) + G.multiply(Jn * Gp)
        return C + C.transpose()

      if motif_type == "struc":
        Gp = mcin._build_Gp(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        C = Gp.multiply(J0 * Gs) + J0.multiply(Gs * Gp) + Gs.multiply(J0 * Gp)
        return C + C.transpose()

  if mam_method == "sparse":
    if mam_weight_type == "unweighted":
      if motif_type == "func":
        Jd = mcin._build_Jd(adj_mat)
        Id = mcin._build_Id(adj_mat)
        J = mcin._build_J(adj_mat)
        C = mcut._a_one_b(Jd, J) - Jd.multiply(J)
        C = C + J * Jd - Id.multiply(J * Jd)
        C = C + mcut._a_one_b(J, Jd) - J.multiply(Jd)
        return sparse.csr_matrix(C + C.transpose())

      if motif_type == "struc":
        Jd = mcin._build_Jd(adj_mat)
        Je = mcin._build_Je(adj_mat)
        Js = mcin._build_Js(adj_mat)
        C = mcut._a_one_b(Jd, Js) - Jd.multiply(Je * Js)
        C = C + Js * Jd - Je.multiply(Js * Jd)
        C = C + mcut._a_one_b(Js, Jd) - Js.multiply(Je * Jd)
        return sparse.csr_matrix(C + C.transpose())

    if mam_weight_type == "mean":
      if motif_type == "func":
        Jd = mcin._build_Jd(adj_mat)
        Gd = mcin._build_Gd(adj_mat)
        Id = mcin._build_Id(adj_mat)
        J = mcin._build_J(adj_mat)
        G = mcin._build_G(adj_mat)
        C = mcut._a_one_b(Jd, G) - Jd.multiply(G) + mcut._a_one_b(Gd, J) - Gd.multiply(J)
        C = C + J * Gd - Id.multiply(J * Gd) + G * Jd - Id.multiply(G * Jd)
        C = C + mcut._a_one_b(J, Gd) - J.multiply(Gd) + mcut._a_one_b(G, Jd) - G.multiply(Jd)
        return sparse.csr_matrix(C + C.transpose()) / 3

      if motif_type == "struc":
        Jd = mcin._build_Jd(adj_mat)
        Gd = mcin._build_Gd(adj_mat)
        Je = mcin._build_Je(adj_mat)
        Js = mcin._build_Js(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        C = mcut._a_one_b(Jd, Gs) - Jd.multiply(Je * Gs)
        C = C + mcut._a_one_b(Gd, Js) - Gd.multiply(Je * Js)
        C = C + Js * Gd - Je.multiply(Js * Gd) + Gs * Jd - Je.multiply(Gs * Jd)
        C = C + mcut._a_one_b(Js, Gd) - Js.multiply(Je * Gd)
        C = C + mcut._a_one_b(Gs, Jd) - Gs.multiply(Je * Jd)
        return sparse.csr_matrix(C + C.transpose()) / 3

    if mam_weight_type == "product":
      if motif_type == "func":
        Gp = mcin._build_Gp(adj_mat)
        Id = mcin._build_Id(adj_mat)
        G = mcin._build_G(adj_mat)
        C = mcut._a_one_b(Gp, G) - Gp.multiply(G)
        C = C + G * Gp - Id.multiply(G * Gp)
        C = C + mcut._a_one_b(G, Gp) - G.multiply(Gp)
        return sparse.csr_matrix(C + C.transpose())

      if motif_type == "struc":
        Gp = mcin._build_Gp(adj_mat)
        Je = mcin._build_Je(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        C = mcut._a_one_b(Gp, Gs) - Gp.multiply(Je * Gs)
        C = C + Gs * Gp - Je.multiply(Gs * Gp)
        C = C + mcut._a_one_b(Gs, Gp) - Gs.multiply(Je * Gp)
        return sparse.csr_matrix(C + C.transpose())


def mam_M13(adj_mat, motif_type, mam_weight_type, mam_method):

  """
  Perform the motif adjacency matrix calculations for motif M13.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  motif_type : str
    Type of motif adjacency matrix to build.
  mam_weight_type : str
    The weighting scheme to use. One of `"unweighted"`, `"mean"` or `"product"`.
  mam_method : str
    Which formulation to use. One of `"dense"` or `"sparse"`.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.
  """

  if mam_method == "dense":
    if mam_weight_type == "unweighted":
      if motif_type == "func":
        Jd = mcin._build_Jd(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        C = Jd.multiply(Jd * Jn)
        Cprime = Jn.multiply(Jd * Jd)
        return C + C.transpose() + Cprime

      if motif_type == "struc":
        Jd = mcin._build_Jd(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        C = Jd.multiply(Jd * J0)
        Cprime = J0.multiply(Jd * Jd)
        return C + C.transpose() + Cprime

    if mam_weight_type == "mean":
      if motif_type == "func":
        Jd = mcin._build_Jd(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        Gd = mcin._build_Gd(adj_mat)
        C = Jd.multiply(Gd * Jn) + Gd.multiply(Jd * Jn) + Jn.multiply(Jd * Gd)
        return (C + C.transpose()) / 4

      if motif_type == "struc":
        Jd = mcin._build_Jd(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        Gd = mcin._build_Gd(adj_mat)
        C = Jd.multiply(Gd * J0) + Gd.multiply(Jd * J0) + J0.multiply(Jd * Gd)
        return (C + C.transpose()) / 4

    if mam_weight_type == "product":
      if motif_type == "func":
        Gp = mcin._build_Gp(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        C = Gp.multiply(Gp * Jn)
        Cprime = Jn.multiply(Gp * Gp)
        return C + C.transpose() + Cprime

      if motif_type == "struc":
        Gp = mcin._build_Gp(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        C = Gp.multiply(Gp * J0)
        Cprime = J0.multiply(Gp * Gp)
        return C + C.transpose() + Cprime

  if mam_method == "sparse":
    if mam_weight_type == "unweighted":
      if motif_type == "func":
        Jd = mcin._build_Jd(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = mcut._a_b_one(Jd, Jd) - Jd.multiply(Jd)
        Cprime = Jd * Jd - Id.multiply(Jd * Jd)
        return sparse.csr_matrix(C + C.transpose() + Cprime)

      if motif_type == "struc":
        Jd = mcin._build_Jd(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = mcut._a_b_one(Jd, Jd) - Jd.multiply(Jd * Je)
        Cprime = Jd * Jd - Je.multiply(Jd * Jd)
        return sparse.csr_matrix(C + C.transpose() + Cprime)

    if mam_weight_type == "mean":
      if motif_type == "func":
        Jd = mcin._build_Jd(adj_mat)
        Gd = mcin._build_Gd(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = mcut._a_b_one(Jd, Gd) - Jd.multiply(Gd) + mcut._a_b_one(Gd, Jd) - Gd.multiply(Jd)
        C = C + Jd * Gd - Id.multiply(Jd * Gd)
        return sparse.csr_matrix(C + C.transpose()) / 4

      if motif_type == "struc":
        Jd = mcin._build_Jd(adj_mat)
        Gd = mcin._build_Gd(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = mcut._a_b_one(Jd, Gd) - Jd.multiply(Gd * Je)
        C = C + mcut._a_b_one(Gd, Jd) - Gd.multiply(Jd * Je)
        C = C + Jd * Gd - Je.multiply(Jd * Gd)
        return sparse.csr_matrix(C + C.transpose()) / 4

    if mam_weight_type == "product":
      if motif_type == "func":
        Gp = mcin._build_Gp(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = mcut._a_b_one(Gp, Gp) - Gp.multiply(Gp)
        Cprime = Gp * Gp - Id.multiply(Gp * Gp)
        return sparse.csr_matrix(C + C.transpose() + Cprime)

      if motif_type == "struc":
        Gp = mcin._build_Gp(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = mcut._a_b_one(Gp, Gp) - Gp.multiply(Gp * Je)
        Cprime = Gp * Gp - Je.multiply(Gp * Gp)
        return sparse.csr_matrix(C + C.transpose() + Cprime)


def mam_Mcoll(adj_mat, motif_type, mam_weight_type, mam_method):

  """
  Perform the motif adjacency matrix calculations for motif Mcoll.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  motif_type : str
    Type of motif adjacency matrix to build.
  mam_weight_type : str
    The weighting scheme to use. One of `"unweighted"`, `"mean"` or `"product"`.
  mam_method : str
    Which formulation to use. One of `"dense"` or `"sparse"`.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.
  """

  if mam_method == "dense":
    if mam_weight_type == "unweighted":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        C = Jn.multiply(J * J.transpose())
        return C

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        C = J0.multiply(Js * Js.transpose())
        return C

    if mam_weight_type == "mean":
      if motif_type == "func":
        G = mcin._build_G(adj_mat)
        J = mcin._build_J(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        C = Jn.multiply(J * G.transpose()) + Jn.multiply(G * J.transpose())
        return C / 2

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        C = J0.multiply(Js * Gs.transpose()) + J0.multiply(Gs * Js.transpose())
        return C / 2

    if mam_weight_type == "product":
      if motif_type == "func":
        G = mcin._build_G(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        C = Jn.multiply(G * G.transpose())
        return C

      if motif_type == "struc":
        Gs = mcin._build_Gs(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        C = J0.multiply(Gs * Gs.transpose())
        return C

  if mam_method == "sparse":
    if mam_weight_type == "unweighted":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = J * J.transpose() - Id.multiply(J * J.transpose())
        return sparse.csr_matrix(C)

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = Js * Js.transpose() - Je.multiply(Js * Js.transpose())
        return sparse.csr_matrix(C)

    if mam_weight_type == "mean":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        G = mcin._build_G(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = J * G.transpose() - Id.multiply(J * G.transpose())
        C = C + G * J.transpose() - Id.multiply(G * J.transpose())
        return sparse.csr_matrix(C) / 2

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = Js * Gs.transpose() - Je.multiply(Js * Gs.transpose())
        C = C + Gs * Js.transpose() - Je.multiply(Gs * Js.transpose())
        return sparse.csr_matrix(C) / 2

    if mam_weight_type == "product":
      if motif_type == "func":
        G = mcin._build_G(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = G * G.transpose() - Id.multiply(G * G.transpose())
        return sparse.csr_matrix(C)

      if motif_type == "struc":
        Gs = mcin._build_Gs(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = Gs * Gs.transpose() - Je.multiply(Gs * Gs.transpose())
        return sparse.csr_matrix(C)


def mam_Mexpa(adj_mat, motif_type, mam_weight_type, mam_method):

  """
  Perform the motif adjacency matrix calculations for motif Mexpa.

  Parameters
  ----------
  adj_mat : matrix
    Adjacency matrix from which to build the motif adjacency matrix.
  motif_type : str
    Type of motif adjacency matrix to build.
  mam_weight_type : str
    The weighting scheme to use. One of `"unweighted"`, `"mean"` or `"product"`.
  mam_method : str
    Which formulation to use. One of `"dense"` or `"sparse"`.

  Returns
  -------
  sparse matrix
    A motif adjacency matrix.
  """

  if mam_method == "dense":
    if mam_weight_type == "unweighted":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        C = Jn.multiply(J.transpose() * J)
        return C

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        C = J0.multiply(Js.transpose() * Js)
        return C

    if mam_weight_type == "mean":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        G = mcin._build_G(adj_mat)
        C = Jn.multiply(J.transpose() * G) + Jn.multiply(G.transpose() * J)
        return C / 2

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        C = J0.multiply(Js.transpose() * Gs) + J0.multiply(Gs.transpose() * Js)
        return C / 2

    if mam_weight_type == "product":
      if motif_type == "func":
        G = mcin._build_G(adj_mat)
        Jn = mcin._build_Jn(adj_mat)
        C = Jn.multiply(G.transpose() * G)
        return C

      if motif_type == "struc":
        Gs = mcin._build_Gs(adj_mat)
        J0 = mcin._build_J0(adj_mat)
        C = J0.multiply(Gs.transpose() * Gs)
        return C

  if mam_method == "sparse":
    if mam_weight_type == "unweighted":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = J.transpose() * J - Id.multiply(J.transpose() * J)
        return sparse.csr_matrix(C)

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = Js.transpose() * Js - Je.multiply(Js.transpose() * Js)
        return sparse.csr_matrix(C)

    if mam_weight_type == "mean":
      if motif_type == "func":
        J = mcin._build_J(adj_mat)
        G = mcin._build_G(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = J.transpose() * G - Id.multiply(J.transpose() * G)
        C = C + G.transpose() * J - Id.multiply(G.transpose() * J)
        return sparse.csr_matrix(C) / 2

      if motif_type == "struc":
        Js = mcin._build_Js(adj_mat)
        Gs = mcin._build_Gs(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = Js.transpose() * Gs - Je.multiply(Js.transpose() * Gs)
        C = C + Gs.transpose() * Js - Je.multiply(Gs.transpose() * Js)
        return sparse.csr_matrix(C) / 2

    if mam_weight_type == "product":
      if motif_type == "func":
        G = mcin._build_G(adj_mat)
        Id = mcin._build_Id(adj_mat)
        C = G.transpose() * G - Id.multiply(G.transpose() * G)
        return sparse.csr_matrix(C)

      if motif_type == "struc":
        Gs = mcin._build_Gs(adj_mat)
        Je = mcin._build_Je(adj_mat)
        C = Gs.transpose() * Gs - Je.multiply(Gs.transpose() * Gs)
        return sparse.csr_matrix(C)
