from typing import Any, Callable, Dict, List
from dataclasses import dataclass
from collections import deque
import importlib

def load_function(name: str) -> Callable:
    path, function = name.rsplit(".", 1)
    module = importlib.import_module(path)
    return getattr(module, function)

@dataclass
class Result:
    success:     bool
    grade:       int
    message:     str

@dataclass
class Arguments:
    args:   List[Any]
    kwargs: Dict[str, Any]

def NotImplemented():
    raise NotImplementedError()

def track_call_count(fn):
    def deco(*args, **kwargs):
        deco.calls += 1
        return fn(*args, **kwargs)
    deco.calls = 0
    return deco

def fetch_tracked_call_count(fn):
    calls = getattr(fn, "calls", 0)
    setattr(fn, "calls", 0)
    return calls

def record_calls(fn):
    def deco(*args, **kwargs):
        deco.calls.append({
            "args": args,
            "kwargs": kwargs
        })
        return fn(*args, **kwargs)
    deco.calls = deque()
    return deco

def fetch_recorded_calls(fn):
    calls = getattr(fn, "calls", deque())
    setattr(fn, "calls", deque())
    return calls

def add_call_listener(listener):
    def decorator(fn):
        def decorated(*args, **kwargs):
            returned = fn(*args, **kwargs)
            listener(returned, *args, **kwargs)
            return returned
        return decorated
    return decorator

class CacheContainer:
    def cache(self) -> Dict[Any, Any]:
        if hasattr(self, "_cache"):
            return getattr(self, "_cache")
        else:
            cache = {}
            setattr(self, "_cache", cache)
            return cache

# Unused
def _cache_function(self) -> Dict[Any, Any]:
    if hasattr(self, "_cache"):
        return getattr(self, "_cache")
    else:
        cache = {}
        setattr(self, "_cache", cache)
        return cache

def with_cache(cls):
    cls.cache = _cache_function
    return cls

class bcolors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'