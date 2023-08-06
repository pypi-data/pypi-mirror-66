# Spawner Python SDK

To get an API key, [sign up here](https://spawner.ai/). Use our API to utomate your trading system, build trading applications, find alpha.

Welcome to the Spawner API! Using our API you can build an entire trading system, from front to back. You can view our full docs [here](https://build.spawner.ai). 

## Requirements

Python 3.x

## Installation

```sh
pip install spawner
```

Then import the package:
```python
import spawner
```

## Getting Started

```python
from spawner.performance import sharpe

token = 'sp_fjznvi393nzkmcizoeo3'
sharpe_ratio = sharpe(token, 'AAPL')
```