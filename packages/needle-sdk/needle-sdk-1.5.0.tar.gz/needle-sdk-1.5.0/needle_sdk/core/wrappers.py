from .classes import RequestData
import threading

wrappers = None
needle_data = threading.local()

# Initialise wrappers
def init_wrapper_store():
    global wrappers

    wrappers = []

    try:
        lang_module = 'django.core.handlers.base.BaseHandler.get_response'
        from django.core.handlers.base import BaseHandler
        add_wrapper_record(lang_module, BaseHandler.get_response, needle_django_get_response)
    except ImportError:
        pass

    try:
        lang_module = 'django.template.loader.render_to_string'
        import django.template.loader
        add_wrapper_record(lang_module, django.template.loader.render_to_string, needle_django_template_render)
    except ImportError:
        pass

    try:
        lang_module = 'flask.signals.request_started'
        add_wrapper_record(lang_module, None, needle_flask_request_started)
    except ImportError:
        pass

    try:
        lang_module = 'flask.signals.request_finished'
        add_wrapper_record(lang_module, None, needle_flask_request_finished)
    except ImportError:
        pass

    try:
        lang_module = 'flask.render_template'
        import flask
        add_wrapper_record(lang_module, flask.render_template, needle_flask_render_template)
    except ImportError:
        pass

    try:
        lang_module = 'mysql.connector.connect'
        import mysql.connector
        add_wrapper_record(lang_module, mysql.connector.connect, needle_mysql_connect)
    except ImportError:
        pass

    try:
        lang_module = 'psycopg2.connect'
        import psycopg2
        add_wrapper_record(lang_module, psycopg2.connect, needle_psycopg2_connect)
    except ImportError:
        pass

    try:
        lang_module = 'os.system'
        import os
        add_wrapper_record(lang_module, os.system, needle_os_system)
    except ImportError:
        pass

    try:
        lang_module = 'os.popen'
        import os
        add_wrapper_record(lang_module, os.popen, needle_os_popen)
    except ImportError:
        pass


# Add wrapper record
def add_wrapper_record(lang_module, orig, wrapper):
    global wrappers
    wrappers.append({'lang_module': lang_module, 'orig': orig, 'wrapper': wrapper})


# Get wrapper
def get_wrapper(lang_module):
    global wrappers
    wrapper = None

    for w in wrappers:
        if w['lang_module'] == lang_module:
            wrapper = w['wrapper']
            break

    return wrapper


# Get wrapper
def get_orig(lang_module):
    global wrappers
    orig = None

    for w in wrappers:
        if w['lang_module'] == lang_module:
            orig = w['orig']
            break

    return orig


# Set wrapper
def set_wrapper(lang_module, set_flag):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    try:
        if set_flag:
            func = get_wrapper(lang_module)
        else:
            func = get_orig(lang_module)

        if lang_module == 'django.core.handlers.base.BaseHandler.get_response':
            try:
                from django.core.handlers.base import BaseHandler
                BaseHandler.get_response = func
            except ImportError:
                pass

        if lang_module == 'django.template.loader.render_to_string':
            try:
                import django.template.loader
                django.template.loader.render_to_string = func
            except ImportError:
                pass

        if lang_module == 'flask.render_template':
            try:
                import flask
                flask.render_template = func
            except ImportError:
                pass

        if lang_module == 'mysql.connector.connect':
            try:
                import mysql.connector
                mysql.connector.connect = func
            except ImportError:
                pass

        if lang_module == 'psycopg2.connect':
            try:
                import psycopg2
                psycopg2.connect = func
            except ImportError:
                pass

        if lang_module == 'os.system':
            try:
                import os
                os.system = func
            except ImportError:
                pass

        if lang_module == 'os.popen':
            try:
                import os
                os.popen = func
            except ImportError:
                pass
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error setting wrapper', error_data)


# Wrapper
def needle_django_get_response(*args, **kwargs):
    py_module = 'django.core.handlers.base.BaseHandler.get_response'
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    try:
        needle_app.total_requests += 1

        request_data = RequestData()

        values = []
        for key, value in args[1].GET.items():
            values.append({'type': 'get', 'name': key, 'value': value})

        for key, value in args[1].POST.items():
            values.append({'type': 'post', 'name': key, 'value': value})

        path_args = args[1].path.split('/')
        for p in path_args:
            if p == '': continue
            values.append({'type': 'path', 'name': 'path', 'value': p})

        request_data.data = values

        request_data.remote_addr = args[1].META['REMOTE_ADDR']
        request_data.request_method = args[1].META['REQUEST_METHOD']
        request_data.http_host = args[1].META['HTTP_HOST']
        request_data.path_info = args[1].META['PATH_INFO']
        request_data.http_user_agent = args[1].META['HTTP_USER_AGENT']

        needle_data.req_data = request_data

        # Check for security scanner
        try:
            sec_module = 'scan'
            scan_check, action = needle_app.module_active(sec_module)
            if scan_check:
                needle_app.inc_mod_requests(sec_module, py_module)
                match, arg_type, arg_name, arg_value = check_sec_scanner()
                if match:
                    if needle_app.debug_mode: print('Needle.sh: New Incident of type: Security scanner')

                    # Save request action to thread-data
                    needle_data.req_data.incident_action = action
                    needle_data.req_data.incident_module = sec_module

                    # Add mal request
                    needle_app.add_mal_request(action, sec_module, arg_type, arg_name, arg_value, needle_data.req_data)

        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error checking security scanner:', error_data)

        # Call original method
        response = get_orig(py_module)(*args, **kwargs)

        # Insert security related HTTP headers
        sec_headers = needle_app.get_sec_headers()
        for i, (key, value) in enumerate(sec_headers.items()):
            response[key] = value

        if len(sec_headers) > 0: needle_app.inc_mod_requests('add_headers', py_module)

        return response
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error while adding request data to thread storage', error_data)


# Save Request Get/Post params
def needle_flask_request_started(*args, **kwargs):
    py_module = 'flask.signals.request_started'

    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    if needle_app.debug_mode: print('Needle.sh: ' + py_module)

    try:
        needle_app.total_requests += 1

        from flask import request

        request_data = RequestData()
        values = []
        get_params = request.args
        for key, value in get_params.items():
            values.append({'type': 'get', 'name': key, 'value': value})

        post_params = request.form
        for key, value in post_params.items():
            values.append({'type': 'post', 'name': key, 'value': value})

        path_args = request.path.split('/')
        for p in path_args:
            if p == '': continue
            values.append({'type': 'path', 'name': 'path', 'value': p})

        request_data.data = values

        request_data.remote_addr = request.remote_addr
        request_data.request_method = request.method
        request_data.http_host = request.host
        request_data.path_info = request.path
        request_data.http_user_agent = request.user_agent.string

        needle_data.req_data = request_data
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error while adding request data to thread storage', error_data)

    try:
        needle_scan_module(py_module)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error while checking sec scanner', error_data)


def needle_flask_request_finished(*args, **kwargs):
    py_module = 'flask.signals.request_finished'

    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    if needle_app.debug_mode: print('Needle.sh: '+py_module)

    response = kwargs['response']

    # Insert security related HTTP headers
    sec_headers = needle_app.get_sec_headers()
    for i, (key, value) in enumerate(sec_headers.items()):
        response.headers[key] = value

    if len(sec_headers) > 0: needle_app.inc_mod_requests('add_headers', py_module)


# Check for security scanner
def needle_scan_module(py_module):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    sec_module = 'scan'

    try:
        scan_check, action = needle_app.module_active(sec_module)
        if scan_check:
            needle_app.inc_mod_requests(sec_module, py_module)
            match, arg_type, arg_name, arg_value = check_sec_scanner()
            if match:

                if needle_app.debug_mode: print('Needle.sh: New Incident of type: Security scanner')

                # Save request action to thread-data
                needle_data.req_data.incident_action = action
                needle_data.req_data.incident_module = sec_module

                # Add mal request
                needle_app.add_mal_request(action, sec_module, arg_type, arg_name, arg_value, needle_data.req_data)

    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking security scanner', error_data)


# Check for XSS attack
def check_content_xss(content):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    match = False
    arg_type = ''
    arg_name = ''
    arg_value = ''

    try:
        libinjec = needle_app.get_libinjec()

        for obj in needle_data.req_data.data:
            value = obj['value']
            if value == '': continue

            if libinjec:
                resp = libinjec.xss(value)
                if resp == 1:
                    # Check if content contains arg value
                    if content.find(value) > -1:
                        match = True
                        arg_type = obj['type']
                        arg_name = obj['name']
                        arg_value = obj['value']

                        return match, arg_type, arg_name, arg_value

            # If XSS not detected using libinjec module, use regex
            if needle_app.debug_mode: print('Checking XSS using regex...')
            xss_pattern = needle_app.get_xss_pattern()

            if xss_pattern:
                if len(xss_pattern.findall(value)) > 0:
                    # Check if content contains arg value
                    if content.find(value) > -1:
                        match = True
                        arg_type = obj['type']
                        arg_name = obj['name']
                        arg_value = obj['value']

                        return match, arg_type, arg_name, arg_value
            else:
                needle_app.add_error('Error checking XSS:', 'XSS pattern unavailable')
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking XSS:', error_data)

    return match, arg_type, arg_name, arg_value


# Monkey patch: Render template function
def needle_django_template_render(*args, **kwargs):
    py_module = 'django.template.loader.render_to_string'

    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    sec_module = 'xss'

    try:
        # Add module used
        needle_app.add_module(sec_module, 'django.template.loader', 'render_to_string')

        # Get HTML content
        content = get_orig(py_module)(*args, **kwargs)

        # Save request action to thread-data
        if needle_data.req_data.incident_action == 'block':
            content = needle_app.get_blocked_page_content(needle_data.req_data.incident_module)
        else:
            # Check if XSS module is active
            xss_check, action = needle_app.module_active(sec_module)
            if xss_check:
                needle_app.inc_mod_requests(sec_module, py_module)
                if needle_app.debug_mode: print('Needle.sh: Checking XSS')

                match, arg_type, arg_name, arg_value = check_content_xss(content)
                if match:
                    if needle_app.debug_mode: print('Needle.sh: New Incident of type: XSS')

                    if action == 'block':
                        # Show blocked message
                        content = needle_app.get_blocked_page_content('xss')

                    # Add mal request
                    needle_app.add_mal_request(action, 'xss', arg_type, arg_name, arg_value, needle_data.req_data)

        return content
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking reflected XSS:', error_data)


# Monkey patch: Render template function
def needle_flask_render_template(*args, **kwargs):
    py_module = 'flask.render_template'

    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    sec_module = 'xss'

    try:
        # Add module used
        needle_app.add_module(sec_module, 'flask', 'render_template')

        # Get HTML content
        content = get_orig(py_module)(*args, **kwargs)

        # Save request action to thread-data
        if needle_data.req_data.incident_action == 'block':
            content = needle_app.get_blocked_page_content(needle_data.req_data.incident_module)
        else:
            # Check if XSS module is active
            xss_check, action = needle_app.module_active(sec_module)
            if xss_check:
                needle_app.inc_mod_requests(sec_module, py_module)
                if needle_app.debug_mode: print('Checking XSS...')

                match, arg_type, arg_name, arg_value = check_content_xss(content)
                if match:
                    if needle_app.debug_mode: print('Needle.sh: New Incident of type: XSS')

                    if action == 'block':
                        # Show blocked message
                        content = needle_app.get_blocked_page_content('xss')

                    # Add mal request
                    needle_app.add_mal_request(action, 'xss', arg_type, arg_name, arg_value, needle_data.req_data)

        return content
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking reflected XSS', error_data)


# Check command injection
def check_command_injection(command):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    match = False
    arg_type = ''
    arg_name = ''
    arg_value = ''

    try:
        cmdi_pattern = needle_app.get_cmdi_pattern()

        if cmdi_pattern:
            for obj in needle_data.req_data.data:
                value = obj['value']
                if value == '': continue

                remove_chars = ['\'', '"', '\\', '$@', '`', '$(', ')']  # Remove characters that will be ignored by command shell
                for c in remove_chars:
                    value = value.replace(c, '')
                    command = command.replace(c, '')

                if value == '': continue

                if len(cmdi_pattern.findall(value)) > 0:
                    # Check if command contains arg value
                    if command.find(value) > -1:
                        match = True
                        arg_type = obj['type']
                        arg_name = obj['name']
                        arg_value = obj['value']
                        return match, arg_type, arg_name, arg_value
        else:
            needle_app.add_error('Error checking command injection:', 'Unavailable cmdi pattern')

    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking command injection', error_data)

    return match, arg_type, arg_name, arg_value


# Check command injection
def needle_cmdi_check(py_module, *args, **kwargs):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    sec_module = 'cmdi'

    # Add module used
    needle_app.add_module(sec_module, '', py_module)

    try:
        cmdi_check, action = needle_app.module_active(sec_module)

        if cmdi_check:
            needle_app.inc_mod_requests(sec_module, py_module)
            match, arg_type, arg_name, arg_value = check_command_injection(args[0])

            if match:
                if needle_app.debug_mode: print('Needle.sh: New Incident of type: Command injection')

                if action == 'block':
                    # Replace with blank command
                    args = ('',)

                    # Save request action to thread-data
                    needle_data.req_data.incident_action = 'block'
                    needle_data.req_data.incident_module = sec_module

                # Add mal request
                needle_app.add_mal_request(action, sec_module, arg_type, arg_name, arg_value, needle_data.req_data)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking command injection', error_data)

    # Call original function
    return get_orig(py_module)(*args, **kwargs)


# Instrumented method for os.system
def needle_os_system(*args, **kwargs):
    try:
        py_module = 'os.system'
        return needle_cmdi_check(py_module, *args, **kwargs)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking command injection', error_data)


# Instrumented method for os.popen
def needle_os_popen(*args, **kwargs):
    try:
        py_module = 'os.popen'
        return needle_cmdi_check(py_module, *args, **kwargs)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking command injection', error_data)


# Check SQL injection
def check_sql_injection(query):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    match = False
    arg_type = ''
    arg_name = ''
    arg_value = ''

    if needle_app.debug_mode: print('Needle.sh: Checking SQL injection...')

    try:
        libinjec = needle_app.get_libinjec()

        for obj in needle_data.req_data.data:
            value = obj['value']

            if value == '': continue

            if libinjec:
                resp = libinjec.sqli(value, '')
                if resp == 1:
                    # Check if SQL query contains arg value
                    if query.find(value) > -1:
                        match = True
                        arg_type = obj['type']
                        arg_name = obj['name']
                        arg_value = obj['value']

                        # Save request action to thread-data
                        needle_data.req_data.incident_action = 'block'
                        needle_data.req_data.incident_module = 'sqli'
                        needle_data.req_data.incident_rule = 'sqli_1'

                        return match, arg_type, arg_name, arg_value

            # If no sql injection detected with libinjection, use regex
            pattern = needle_app.get_sqli_pattern()

            if len(value.split()) > 1 and len(pattern.findall(value)) > 0 and query.find(value) > -1:
                match = True
                arg_type = obj['type']
                arg_name = obj['name']
                arg_value = obj['value']

                # Save request action to thread-data
                needle_data.req_data.incident_action = 'block'
                needle_data.req_data.incident_module = 'sqli'
                needle_data.req_data.incident_rule = 'sqli_2'

                return match, arg_type, arg_name, arg_value

    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking SQL injection:', error_data)

    return match, arg_type, arg_name, arg_value


# Instrumented function for mysql.connection.cursor.execute
def needle_sql_cursor_execute(*args, **kwargs):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    sec_module = 'sqli'
    # Add module used
    needle_app.add_module(sec_module, 'mysql.connection.cursor', 'execute')

    try:
        # Check for SQL injection
        sqli_check, action = needle_app.module_active(sec_module)
        if sqli_check:
            needle_app.inc_mod_requests(sec_module, 'mysql.connection.cursor')
            match, arg_type, arg_name, arg_value = check_sql_injection(args[0])
            if match:
                if needle_app.debug_mode: print('Needle.sh: New Incident of type: SQL injection (rule: '+needle_data.req_data.incident_rule+')')

                if action == 'block':
                    # Change query to blank query
                    args = ('-- Query blocked by Needle.sh agent (Possible SQL injection)',)

                # Add mal request
                needle_app.add_mal_request(action, sec_module, arg_type, arg_name, arg_value, needle_data.req_data)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking SQL injection', error_data)

    return needle_app.orig_sql_cursor_execute(*args, **kwargs)


# Wrapper class around mysql.connection.cursor
class NeedleSqlCursor():
    def __init__(self, cursor):
        from .needle_app import get_needle_app
        needle_app = get_needle_app()
        try:
            self.cursor = cursor
            # self.execute = patcher(self.cursor.execute)
            needle_app.orig_sql_cursor_execute = self.cursor.execute
            self.execute = needle_sql_cursor_execute
        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error initialising cursor object:', error_data)

    def __getattr__(self, name):
        try:
            return getattr(self.cursor, name)
        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error returning custom cursor method:', error_data)


# Wrapper class around mysql.connection
class NeedleSqlConnection():
    def __init__(self, connection):
        from .needle_app import get_needle_app
        needle_app = get_needle_app()

        try:
            self.connection = connection
        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error initialising custom SQL connection object:', error_data)

    def cursor(self, *args, **kwargs):
        from .needle_app import get_needle_app
        needle_app = get_needle_app()

        try:
            orig_cursor = self.connection.cursor(*args, **kwargs)
            return NeedleSqlCursor(orig_cursor)
        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error getting cursor object from SQL connection:', error_data)

    # Handle unknown method calls
    def __getattr__(self, name):
        from .needle_app import get_needle_app
        needle_app = get_needle_app()

        try:
            return getattr(self.connection, name)
        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error returning custom connection method:', error_data)


# Instrumented function for MySQL connect
def needle_mysql_connect(*args, **kwargs):
    py_module = 'mysql.connector.connect'

    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    try:
        conn = get_orig(py_module)(*args, **kwargs)
        return NeedleSqlConnection(conn)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error in instrumented MySQL connect:', error_data)


# Instrumented function for MySQL connect
def needle_psycopg2_connect(*args, **kwargs):
    py_module = 'psycopg2.connect'

    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    try:
        # conn = needle_app.orig_mysql_connect(*args, **kwargs)
        conn = get_orig(py_module)(*args, **kwargs)
        return NeedleSqlConnection(conn)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error in instrumented psycopg2 connect:', error_data)


# Check security scanner
def check_sec_scanner():
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    match = False
    arg_type = ''
    arg_name = ''
    arg_value = ''

    if needle_app.debug_mode: print('Needle.sh: Checking security scanner...')

    try:
        scan_pattern = needle_app.get_scanner_pattern()
        if not scan_pattern: return match, arg_type, arg_name, arg_value

        value = needle_data.req_data.http_user_agent

        if value == '': return match, arg_type, arg_name, arg_value

        if len(scan_pattern.findall(value)) > 0:
            match = True
            arg_type = 'http_header'
            arg_name = 'user_agent'
            arg_value = value

            return match, arg_type, arg_name, arg_value

    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking security scanner:', error_data)

    return match, arg_type, arg_name, arg_value
