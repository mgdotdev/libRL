class TestMainReflectionLoss:
    def test_main_reflection_loss(self, run_patch_and_catch):
        args, kwargs = run_patch_and_catch(
            "libRL.reflection_loss",
            ["libRL", "rl", "path/to/file.csv", "-f", "1,18,0.1", "-d", "0,20,0.1"],
            dict(f=[1], d=[1], RL=[[1]]),
        )

        assert args == ("path/to/file.csv",)
        assert kwargs == {
            "f_set": (1.0, 18.0, 0.1),
            "d_set": (0.0, 20.0, 0.1),
            "override": None,
            "save": None,
        }

    def test_defaults(self, run_patch_and_catch):
        args, kwargs = run_patch_and_catch(
            "libRL.reflection_loss",
            ["libRL", "rl", "path/to/file.csv",],
            dict(f=[1], d=[1], RL=[[1]]),
        )
        assert args == ("path/to/file.csv",)
        assert kwargs == {
            "d_set": (0, 5, 0.1),
            "f_set": None,
            "save": None,
            "override": None,
        }


class TestMainBandAnalysis:
    def test_default_band_analysis(self, run_patch_and_catch):
        args, kwargs = run_patch_and_catch(
            "libRL.band_analysis",
            [
                "libRL",
                "ba",
                "path/to/file.csv",
                "-f",
                "1,18,0.1",
                "-d",
                "0,20,0.1",
                "-m",
                "1,5",
            ],
            {1: {1: 1}},
        )
        assert args == ("path/to/file.csv",)
        assert kwargs == {
            "d_set": (0.0, 20.0, 0.1),
            "m_set": (1.0, 5.0),
            "f_set": (1.0, 18.0, 0.1),
            "save": None,
            "threshold": -10,
        }

    def test_defaults(self, run_patch_and_catch):
        args, kwargs = run_patch_and_catch(
            "libRL.band_analysis", ["libRL", "ba", "path/to/file.csv",], {1: {1: 1}},
        )

        assert args == ("path/to/file.csv",)
        assert kwargs == {
            "d_set": (0, 5, 0.1),
            "m_set": [1],
            "f_set": None,
            "save": None,
            "threshold": -10,
        }


class TestMainCharacterization:
    def test_main_characterization(self, run_patch_and_catch):
        args, kwargs = run_patch_and_catch(
            "libRL.characterization",
            ["libRL", "char", "path/to/file.csv", "-f", "1,18,0.1"],
            {"f": [1, 2, 3], "Qe": [1, 2, 3]},
        )

        assert args == ("path/to/file.csv",)
        assert kwargs == {
            "f_set": (1.0, 18.0, 0.1),
            "params": ["all"],
            "save": None,
        }

    def test_defaults(self, run_patch_and_catch):
        args, kwargs = run_patch_and_catch(
            "libRL.characterization",
            ["libRL", "c", "path/to/file.csv",],
            {"f": [1, 2, 3], "Qe": [1, 2, 3]},
        )
        assert args == ("path/to/file.csv",)
        assert kwargs == {
            "f_set": None,
            "params": ["all"],
            "save": None,
        }
