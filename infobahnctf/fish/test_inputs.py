from fish import Interpreter
import threading

code = open('chall.txt').read()

def run_interp(test_input, result_container):
    try:
        interp = Interpreter(code, test_input)
        output = interp.execute()
        result_container['output'] = output
    except Exception as e:
        result_container['error'] = str(e)

for test_input in ["", "0", "1", "121", "320"]:
    print(f"\n{'='*60}")
    print(f"Testing with input: '{test_input}'")
    print('='*60)
    
    result = {}
    thread = threading.Thread(target=run_interp, args=(test_input, result))
    thread.daemon = True
    thread.start()
    thread.join(timeout=5)
    
    if thread.is_alive():
        print("Timed out after 5 seconds")
    elif 'error' in result:
        print(f"Error: {result['error']}")
    elif 'output' in result:
        output = result['output']
        print(f"Output: {output}")
        print(f"Reversed: {output[::-1]}")
        print(f"Wrapped: infobahn{{{output[::-1]}}}")
