try:
    from libRL.tools._extensions import gamma, test_extension
except ImportError:
    from libRL.tools.redundancies import gamma, test_extension
