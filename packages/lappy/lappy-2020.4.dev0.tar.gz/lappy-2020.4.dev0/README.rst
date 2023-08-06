Lappy
=====

``Lappy`` is a fork of Sophia Lin's ``lazyray`` that supports more operations beyond arithmetics.

In ``Lappy``, everything computable is considered an array object (unlike ``numpy``, it does not offer separate scalar types).
An array object has six basic components: the shape, the dtype, the expression, the value, the formal argument list, and the environment (capture list).
Scalars are special arrays with shape being an empty tuple.
If the dtype is an integer type, there can be assumptions associated with the array elements represented by an integer set (for scalars) or map (for non-scalars).

Documentation
-------------

Please visit `<https://xiaoyu-wei.com/docs/lappy/>`_ for the latest documentation.

Status
------

This is a list of things that can be achieved with ``lappy`` today:

- ✅ Arithmetic and scalar mathematics (lifted scalar functions / universal functions)
- ✅ Axis reordering / transpose
- ✅ Reshaping
- ✅ Broadcasting (semi-dynamic)

Scope
-----

Roadmap
*******

- ✅ Scan and fold
- ✅ Tensor contractions, like ``np.einsum`` (including dot products and matrix multiply)
- ✅ Slicing (static and dynamic)
- ✅ Fancy indexing (static and dynamic)
- ✅ Integration with Numpy's dispatch mechanism like ``__array__`` and ``__array_ufunc__``
- ✅ Some linear algebra like ``svd``, ``qr``, ``lstsq``

Anti-features
*************

- ❌ Another array IR like APL. ``lappy`` is not an IR and does not intend to be.
     It serves as a tool to build parametrized array expressions for lazy evaluation,
     and strives to provide ``numpy`` compatible APIs.

----

``Lappy`` is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_ and free for commercial, academic,
and private use.
