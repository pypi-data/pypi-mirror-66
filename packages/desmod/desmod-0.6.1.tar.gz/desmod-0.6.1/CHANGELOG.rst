Changelog
=========

desmod-0.6.1 (2020-04-16)
-------------------------
* [FIX] Pool when_not_full and when_not_empty broken epsilon
* [FIX] Typing for SimEnvironment.time()
* [FIX] Typing for __exit__() methods

desmod-0.6.0 (2020-04-07)
-------------------------
* [BREAK] Drop support for Python < 3.6
* [NEW] Inline type annotations
* [FIX] Use yaml.safe_load() in tests

desmod-0.5.6 (2019-02-12)
-------------------------
* [NEW] PriorityPool for prioritized get/put requests
* [NEW] Queue.when_at_most() and when_at_least() events (#18)
* [NEW] Pool.when_at_most() and when_at_least() events (#18)
* [CHANGE] Remove Queue.when_new() event
* [CHANGE] Gas station example uses Pool/Pool.when_at_most() (#18)
* [FIX] Add API docs for desmod.pool

desmod-0.5.5 (2018-12-19)
-------------------------
* [NEW] Add Queue.when_not_full() and Pool.when_not_full()
* [NEW] Context manager protocol for Queue and Pool
* [CHANGE] Pool checks validity of get/put amounts
* [CHANGE] Pool getters/putters are not strictly FIFO
* [CHANGE] __repr__() for Queue and Pool
* [FIX] Pool no longer allows capacity to be exceeded
* [FIX] Pool and Queue trigger all getters and putters
* [FIX] Pool and Queue trigger from callbacks
* [FIX] Repair deprecated import from collections
* [FIX] Various Pool docstrings
* [FIX] Complete unit test coverage for Queue and Pool

desmod-0.5.4 (2018-08-20)
-------------------------
* [NEW] Add desmod.pool.Pool for modeling pool of resources

desmod-0.5.3 (2018-05-25)
-------------------------
* [FIX] Repair silent truncation of config override
* [CHANGE] Update dev requirements
* [CHANGE] Do not use bare except
* [CHANGE] Modernize travis-ci config

desmod-0.5.2 (2017-09-08)
-------------------------
* [FIX] Join worker processes in simulate_many()
* [FIX] Ensure PriorityQueue's items are heapified

desmod-0.5.1 (2017-04-27)
-------------------------
* [NEW] Add config_filter param to simulate_factors() (#14)
* [FIX] Use pyenv for travis builds

desmod-0.5.0 (2017-04-27)
-------------------------
* [NEW] Add desmod.dot.generate_dot()
* [NEW] Add "persist" option for tracers
* [NEW] Add SQLiteTracer
* [NEW] Add grocery store example
* [NEW] Support probing a Resource's queue
* [FIX] Stable sort order in DOT generation
* [CHANGE] Rearrange doc index page
* [CHANGE] Change examples hierarchy
* [CHANGE] Add DOT to Gas Station example
* [CHANGE] Tests and cleanup for desmod.probe

desmod-0.4.0 (2017-03-20)
-------------------------
* [CHANGE] meta.sim.index and meta.sim.special
* [CHANGE] Add meta.sim.workspace
* [FIX] Check simulate_many() jobs
* [CHANGE] Add named configuration categories and doc strings

desmod-0.3.3 (2017-02-28)
-------------------------
* [CHANGE] Make NamedManager.name() deps argument optional
* [FIX] Add test for desmod.config.parse_user_factors()
* [FIX] More testing for tracer.py

desmod-0.3.2 (2017-02-24)
-------------------------
* [FIX] Documentation repairs for desmod.config
* [FIX] Add tests for sim.config.file
* [FIX] Annotate no coverage line in test_dot.py
* [NEW] Add desmod.config.apply_user_config()
* [NEW] Support dumping JSON or Python config and result

desmod-0.3.1 (2017-02-10)
-------------------------
* [NEW] Add sim.vcd.start_time and sim.vcd.stop_time
* [NEW] Add unit tests for desmod.tracer
* [NEW] Dump configuration to file in workspace
* [NEW] Add unit tests for desmod.dot
* [FIX] Use component scope instead of id() for DOT nodes
* [NEW] Colored component hierarchy in DOT
* [FIX] Repair typo in fuzzy_match() exception

desmod-0.3.0 (2017-01-23)
-------------------------
* [CHANGE] Overhaul progress display
* [NEW] Flexible control of simulation stop criteria
* [FIX] Support progress notification on spawned processes
* [FIX] Remove dead path in test_simulation.py
* [FIX] Various doc repairs to SimEnvironment
* [CHANGE] Add t parameter to SimEnvironment.time()
* [CHANGE Parse unit in SimEnvironment.time()
* [NEW] Add desmod.config.fuzzy_match()
* [REMOVE] Remove desmod.config.short_special()
* [NEW] Add coveralls to travis test suite
* [NEW] Add flush() to tracing subsystem
* [CHANGE] Do not use tox with travis
* [NEW] Add Python 3.6 support in travis
* [FIX] Repair gas_station.py for Python 2

desmod-0.2.0 (2016-10-25)
-------------------------
* [CHANGE] simulate_factors() now has factors parameter
* [NEW] simulate() can suppress exceptions
* [FIX] simulate_factors() respects sim.workspace.overwrite
* [CHANGE] Update config with missing defaults at runtime

desmod-0.1.6 (2016-10-25)
-------------------------
* [NEW] Add env.time() and 'sim.now' result
* [FIX] Enter workspace directory before instantiating env
* [CHANGE] Use yaml.safe_dump()
* [FIX] Add dist to .gitignore
* [FIX] Squash warning in setup.cfg

desmod-0.1.5 (2016-10-17)
-------------------------
* [NEW] Add Queue.size and Queue.remaining properties (#9)
* [NEW] Trace Queue's remaining capacity (#10)
* [NEW] Add Queue.when_new() event (#11)

desmod-0.1.4 (2016-09-21)
-------------------------
* [NEW] Add desmod.simulation.simulate_many()
* [FIX] Repair various docstring typos
* [FIX] Disable progress bar for simulate_factors() on Windows
* [NEW] Add CHANGELOG.txt to long description in setup.py

desmod-0.1.3 (2016-07-28)
-------------------------
* [NEW] Cancelable Queue events
* [CHANGE] Connection errors now raise ConnectError
* [FIX] Update pytest-flake8 and flake8 dependencies (yet again)

desmod-0.1.2 (2016-07-26)
-------------------------
* [NEW] Add "sim.log.buffering" configuration
* [FIX] Repair unit tests (pytest-flake8 dependency)
* [NEW] New optional `Queue.name` attribute
* [FIX] Use `repr()` for exception string in result dict

desmod-0.1.1 (2016-07-14)
-------------------------
* [FIX] Using 'True' and 'False' in expressions from the command line
* [CHANGE] Improve simulation workspace handling (sim.workspace.overwrite)
* [CHANGE] Make some 'sim.xxx' configuration keys optional
* [NEW] Gas Station example in docs
* [NEW] Add this CHANGELOG.rst and History page in docs

desmod-0.1.0 (2016-07-06)
-------------------------
* Initial public release
