"""
Unit tests for autodiff engine
"""

# pylint: disable=missing-docstring

from pyfit.engine import Scalar


def test_scalar() -> None:
    x = Scalar(1.0)
    y = (x * 2 + 1).relu()
    assert y.data == 3
    y.backward()
    assert x.grad == 2  # dy/dx


def test_scalar_sub() -> None:
    x = Scalar(2.5)
    y = Scalar(3.5)

    z = x - y
    assert z.data == -1
    z.backward()
    assert x.grad == 1  # dz/dx
    assert y.grad == -1  # dz/dy

    # Reset gradients
    x.grad = 0
    y.grad = 0

    z = y - x
    assert z.data == 1
    z.backward()
    assert x.grad == -1  # dz/dx
    assert y.grad == 1  # dz/dy

    # Reset gradient
    x.grad = 0

    z = x - 3
    assert z.data == -0.5
    z.backward()
    assert x.grad == 1  # dz/dx

    # Reset gradient
    x.grad = 0

    z = 3 - x
    assert z.data == 0.5
    z.backward()
    assert x.grad == -1  # dz/dx


def test_scalar_div() -> None:
    x = Scalar(1.0)
    y = Scalar(4.0)

    z = x / y
    assert z.data == 0.25
    z.backward()
    assert x.grad == 0.25  # dz/dx
    assert y.grad == -0.0625  # dz/dy

    # Reset gradients
    x.grad = 0
    y.grad = 0

    z = y / x
    assert z.data == 4
    z.backward()
    assert x.grad == -4  # dz/dx
    assert y.grad == 1  # dz/dy

    # Reset gradient
    x.grad = 0

    z = x / 3
    assert z.data == 1 / 3
    z.backward()
    assert x.grad == 1 / 3  # dz/dx

    # Reset gradient
    x.grad = 0

    z = 3 / x
    assert z.data == 3
    z.backward()
    assert x.grad == -3  # dz/dx
