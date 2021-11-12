import cmath


def test_extension():
    return 0


def gamma(f, d, e1, e2, mu1, mu2):
    return [
        reflection_loss_function(*[params[0], param, *params[1:]])
        for param in d
        for params in zip(f, e1, e2, mu1, mu2)
    ]


def reflection_loss_function(f, d, e1, e2, mu1, mu2):
    y = 20 * cmath.log10(
        (
            abs(
                (
                    (
                        1
                        * (
                            cmath.sqrt(
                                (mu1 - cmath.sqrt(-1) * mu2)
                                / (e1 - cmath.sqrt(-1) * e2)
                            )
                        )
                        * (
                            cmath.tanh(
                                cmath.sqrt(-1)
                                * (
                                    2
                                    * cmath.pi
                                    * (f * 10 ** 9)
                                    * (d * 0.001)
                                    / 299792458
                                )
                                * cmath.sqrt(
                                    (mu1 - cmath.sqrt(-1) * mu2)
                                    * (e1 - cmath.sqrt(-1) * e2)
                                )
                            )
                        )
                    )
                    - 1
                )
                / (
                    (
                        1
                        * (
                            cmath.sqrt(
                                (mu1 - cmath.sqrt(-1) * mu2)
                                / (e1 - cmath.sqrt(-1) * e2)
                            )
                        )
                        * (
                            cmath.tanh(
                                cmath.sqrt(-1)
                                * (
                                    2
                                    * cmath.pi
                                    * (f * 10 ** 9)
                                    * (d * 0.001)
                                    / 299792458
                                )
                                * cmath.sqrt(
                                    (mu1 - cmath.sqrt(-1) * mu2)
                                    * (e1 - cmath.sqrt(-1) * e2)
                                )
                            )
                        )
                    )
                    + 1
                )
            )
        )
    )
    return [y.real, f, d]
