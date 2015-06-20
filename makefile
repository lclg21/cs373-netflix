FILES :=                              \
    .travis.yml                       \
    netflix-tests/ll9338-RunNetflix.in   \
    netflix-tests/ll9338-RunNetflix.out  \
    netflix-tests/ll9338-TestNetflix.py  \
    netflix-tests/ll9338-TestNetflix.out \
    Netflix.html                      \
    Netflix.log                       \
    Netflix.py                        \
    RunNetflix.py                     \
    RunNetflix.in                     \
    RunNetflix.out                    \
    TestNetflix.py                    \
    TestNetflix.out

all:

check:
	@for i in $(FILES);                                         \
    do                                                          \
        [ -e $$i ] && echo "$$i found" || echo "$$i NOT FOUND"; \
    done

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -f  Netflix.html
	rm -f  Netflix.log
	rm -f  RunNetflix.out
	rm -f  TestNetflix.out
	rm -rf __pycache__

config:
	git config -l

test: RunNetflix.out TestNetflix.out

netflix-tests:
	git clone https://github.com/cs373-summer-2015/netflix-tests.git

Netflix.html: Netflix.py
	pydoc3 -w Netflix

Netflix.log:
	git log > Netflix.log

RunNetflix.out: RunNetflix.py
	cat RunNetflix.in
	./RunNetflix.py < RunNetflix.in > RunNetflix.out
	cat RunNetflix.out

TestNetflix.out: TestNetflix.py
	coverage3 run    --branch TestNetflix.py >  TestNetflix.out 2>&1
	coverage3 report -m                      >> TestNetflix.out
	cat TestNetflix.out

