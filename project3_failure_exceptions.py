def api_failure(status, url, *args):
    '''
    This function prints the failure output, given a status code, url, and optional
    argument which indicates that format was not as expected.
    '''

    print('FAILURE')
    if type(status) == int:
        print(status, url)
    if fail != 200:
        print('NOT 200')
    elif status == None:
        print(url)
        print('NETWORK')

    if 'FORMAT' in args:
        print(status, url)
        print('FORMAT')


def file_failure(path, fail):
    '''Given a path and the type of failure, prints the failure output.'''
    
    print('FAILED')
    print(path)
    print(fail)
