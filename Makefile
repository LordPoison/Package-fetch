PYTHON = python3

.PHONY: all
all: all-scenarios


.PHONY: scenario1
scenario1:
	$(PYTHON) Scenario1.py

.PHONY: scenario1-stochastic
scenario1-stochastic:
	$(PYTHON) Scenario1.py --stochastic

.PHONY: scenario2
scenario2:
	$(PYTHON) Scenario2.py

.PHONY: scenario2-stochastic
scenario2-stochastic:
	$(PYTHON) Scenario2.py --stochastic

.PHONY: scenario3
scenario3:
	$(PYTHON) Scenario3.py

.PHONY: scenario3-stochastic
scenario3-stochastic:
	$(PYTHON) Scenario3.py --stochastic


.PHONY: all-scenarios
all-scenarios: scenario1 scenario2 scenario3


.PHONY: clean
clean:
	rm -f *.png
	rm -rf __pycache__
	rm -f *.pyc