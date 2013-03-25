def ExpectedToFail(fn):
    test = fn()
    test.runTest()
