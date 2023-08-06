Python ``raise`` as a Function
==============================

Raise exceptions with a function instead of a statement.

Provides a minimal, clean and portable interface for raising
exceptions with all the advantages of functions over syntax.


Why
---

I want to be able to work with exceptions in a way that is:

1. *Intuitive* to use and see in code.
2. *Generic* and *flexible*, empowering *reuse* and *composition*.
3. *Portable* to all versions of Python I might want to use.

In my code, I've often found myself writing interfaces that combine
the intuitive nature of Python 3's ``raise`` and ``with_traceback``,
the generic and flexible pattern of raising exceptions in other
coroutines or threads of execution as exemplified by the ``throw``
method on Python generators, and the inherently portable and
powerfully reusable and composable form of a basic function.

The interface provided by this module, the function signature taking
an ``exception`` (either an instance *or* a type) and an optional
``traceback`` instance, is what I found myself arriving at that met all
of these criteria. It has served me well in code that I've worked on,
and I'm submitting it to the world in the hope that others will either
find it useful and build upon it or point out flaws in my approach.

If you have a more specific "why" question, I recorded my reasons for a
lot of the specific choices here in the `Design Decisions`_ section.


Versioning
----------

This library's version numbers follow the `SemVer 2.0.0 specification
<https://semver.org/spec/v2.0.0.html>`_.

The current version number is available in the variable ``__version__``
as is normal for Python modules.


Installation
------------

::

    pip install raise

**If** you need or want to get it *manually*, or you need
the "no traceback" variant, see the `Advanced/Manual
Installation`_ section for suggestions/tips.


Usage
-----

Import the ``raise_`` function from the ``raise_`` module:

.. code:: python

    from raise_ import raise_

Then you can raise things as you'd expect:

1. Raising an exception:

   .. code:: python

       raise_(Exception('foo'))

   (You can also pass an exception type instead of an
   instance as the first argument to ``raise_``.)

2. Raising an exception with a traceback:

   .. code:: python

       raise_(Exception('foo'), my_traceback_object)


Portability
-----------

Portable to all releases of both Python 3 and Python 2.

(The oldest tested is 2.5, but it will likely work on all
Python 2 versions and probably on even earlier versions.)

For implementations of Python that do not support raising with a custom
traceback, a "no traceback" variant can be installed manually.


Advanced/Manual Installation
----------------------------

There are three recommended ways of installing this manually, depending
on your needs:

1. If it does **not** need to be imported by different incompatible
   Python versions, then you can just take either ``raise_3.py`` or
   ``raise_2.py`` and save it as ``raise_.py``.

2. If you're using a Python implementation that does not support raising
   exceptions with a custom traceback, take the ``raise_no_traceback.py``
   file and save it as ``raise_.py``.

2. If you need the same file to be importable into more than one of the
   above, combine the files you need either into one ``raise_.py`` file
   or into one ``raise_`` directory with an ``__init__.py``.

That way you can always do ``from raise_ import raise_`` and it'll
just work, without version-detecting boilerplate or the file names
(which are an implementation detail) leaking into your other code.

You are of course welcome to just copy-paste the tiny ``raise_`` function
definition into your code, just keep in mind the compatibility issues
involved: your code will only work without modification on Python
versions compatible with the version you chose, and Python 2's version
causes a SyntaxError in Python 3, which is uncatchable unless you import
it from another file or wrap that function definition in an ``exec``.


Design Decisions
----------------

* Allowing ``exception`` to be either an instance or a type, because
  it is sometimes useful and is *very* ingrained in Python.

* Not currently implementing an equivalent to
  Python 3's ``except ... from ...`` syntax.

  Ultimately, this syntax just assigns one exception
  as an attribute on another exception.

  This strikes me as *complecting* two different jobs together:
  raising an exception instance and *initializing* an
  exception instance with a ``__cause__`` attribute.

  I note that generators' ``throw`` method does not have support
  for a separe "from"/"cause" argument either. Perhaps it should,
  but then everything implementing this interface would have to
  implement extra logic to handle that extra argument.

  Instead I would advocate for a separate interface for setting the
  ``__cause__`` or ``__context__`` attributes on exceptions.

* Not using the convention of taking separate ``type`` and ``value``
  arguments because it seems like a counter-intuitive and
  inappropriate convention for *raising* an exception.
  (It is a good pattern for functions that *receive* exceptions.)
  
  Python 3 dropped support for separate ``type`` and ``value``
  from the ``raise`` statement, so it seems enough people
  responsible for the language agree with this assessment.

  Also fully/properly supporting all semantics/variations that ``raise``
  allowed before Python 3 would bloat the code excessively.

* Not supporting Python 3's behavior of using the exception's
  ``__traceback__`` attribute as the traceback to raise with
  by default if no traceback is specified.

  Not trying to emulate it in Python 2 and intentionally suppressing
  it in Python 3 by always calling ``.with_traceback`` and using
  ``None`` as the default traceback argument, because:

  * When an insufficiently careful coder (almost all of us almost all
    of the time) has code work one way on one platform, they assume
    it will work that way consistently on other platforms.

  * Not suppressing this behavior requires more code and complicating
    the interface - some other default value for the traceback
    argument besides ``None`` is needed instead (``...``, also known
    as ``Ellipsis``, is a good candidate).

  * Emulating Python 3's behavior on Python 2, would create extra
    potential for **wrong** behavior: any ``except`` that catches
    an exception without updating the ``__traceback__`` before
    passing it to code that relies on it will result in really
    misleading gaps in the traceback.

  * Emulating Python 3's behavior on the "no traceback" Pythons has
    similar difficulty, except even worse: some of those Python
    implementations don't even have a way of adding attributes to
    native exceptions, so the amount of boilerplate to achieve it
    and edge cases to consider goes up even higher.

  * If it differs across implementations, people will get it wrong.
    Simplicity and consistency that covers most cases is valuable.
    Portable correctness is a priority goal here, and gracefully
    degrading in this case would do more harm than good.

  * It is trivial to implement a way to do this as needed which would
    be composable with ``raise_`` or build on top of ``raise_``.

* Using different implementation files for Python 3+ and 2- because:

  1. nesting code in `exec` makes the code less readable and
     harder to consciously and programmmatically verify,

  2. I wanted the implementations for each version of the language
     to be *independently* reusable from a trivial copy-paste,

  3. not having code for conditional imports means
     smaller surface area for bugs, *and*

  4. it allows for cleaner packages and installs.

* Not providing a single file which can be imported on some combination
  of Python 3+, Python 2-, and "no traceback" Python implementations -
  for now - because the need for each permutation seems improbable,
  neither permutation is particularly more likely, and it is fairly
  easy for a developer to combine the files as needed if it comes up.

* Using an affirmative result from ``issubtype`` to decide whether to
  call ``exception`` to construct an instance, even though this
  forces calling ``isinstance`` first to avoid a spurious ``TypeError``, 
  because otherwise arbitrary callables would work for ``exception``,
  which would be inconsistent with that not working for ``traceback``.

  If someone really wants function arguments to accept arbitrary
  callables that will be called when they are used, that is a
  generic feature that can be easily implemented separately, as
  a wrapper for ``raise_``, or in a generic way that may already
  exist in a functional programming or lazy evaluation library.

* To aid portability of code to Python implementations that do not
  support specifying a custom traceback when raising, allowing
  ``traceback`` to be silently accepted but ignored helps writing code
  that portably follows "progressive enhancement" or "graceful
  degradation" practices: tracebacks are properly used where possible,
  but ignored where not.

  This is **not** always the wisest choice: some features and behavior
  are relied on for security, correctness, or debugging, and in those
  cases the inability to fulfill the contract of an interface must not
  be silently hidden.

  Because of this, the "no traceback" variant is "opt-in": if you're
  using it, you deliberately included it into your project, or a
  dependency of yours did.

* Nulling out *both* arguments in the ``finally`` inside of ``raise_``
  to alleviate the potential for reference cycles being made by the
  traceback, which references all locals in each stack frame.

  ``traceback`` is obvious: it will cyclically reference itself.

  ``exception`` **might** reference ``traceback`` either directly or
  indirectly, and we have no way to know for sure that it doesn't.

* Not nulling out the arguments to ``raise_`` in the "no traceback"
  variant because the reference cycle depends on having a reference
  to the traceback data within the call stack itself.

  Also, Python implementations that need the "no traceback" variant
  tend to be diversely incompatible: even ``try``-``finally`` does
  not work in all of them.

  So it seems like the "no traceback" variant doesn't need this fix,
  and it is a safer bet to not mess with it until a need is found.


Scope
-----

This package provides the *bare minimum* needed to support the
"``raise`` as a function" approach *portably* and *correctly*.

In particular, Python syntax for raising an exception with
a custom traceback is simply incompatible between Python 3
and Python 2, and the only way around it is **both**

1. ``exec`` *or* separate files for ``import``, and
2. catching syntax errors *or* version checking.

So code belongs in here if it protects users from having to code
workarounds at least approximately that bad, for problems that
cannot be better solved by a different design or library.

Everything beyond that is probably out-of-scope.
