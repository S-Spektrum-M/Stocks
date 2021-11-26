# S.T.O.C.K.S.

## Installation

Install S.T.O.C.K.S
```bash
    pip3 install robin-stocks
    pip3 install numpy
    pip3 install flask
    git clone https://github.com/S-Spektrum-M/Stocks
    cd Stocks
    touch auth.py
    sudo add-apt-repository ppa:redislabs/redis
    sudo apt-get update
    sudo apt-get install redis
    pip install redis
```
- Add your robinhood email and password to ``auth.py``

## How it works
- S.T.O.C.K.S parses historical data to create two types of models
    - Short term: Linear
    - Long term: Exponential
- If the query has already been served within the last minute then it is loaded from a redis db to increase
  speed and decrease compute time

## API Reference
|   Endpoint   |    Parameter   | Return |        Description       |
|--------------|----------------|--------|--------------------------|
|``/api/short``|``?id={ticker}``|Below   |The short term calculation|
|``/api/long`` |``?id={ticker}``|Below   |The long term calculation |

- Short Return Type
```json
{
  "lower": 2944.7089259649783,
  "upper": 3065.440437798343
}
```
- Long Return Type
```json
{
  "lower": 2944.7089259649783,
  "upper": 3065.440437798343
}
```

## Acknowledgements

- [robin-stocks](https://github.com/jmfernandes/robin_stocks)
- [numpy](https://github.com/jmfernandes/robin_stocks)
- [flask](https://github.com/jmfernandes/robin_stocks)
- [Robinhood](https://robinhood.com/)
- [Redis](https://redis.io/)
- [Redis-py](https://github.com/redis/redis-py)

## License

- [MIT](https://choosealicense.com/licenses/mit/)
- [Robinhood Financial LLC & Robinhood Securities, LLC  Customer Agreement](https://cdn.robinhood.com/assets/robinhood/legal/Robinhood%20Customer%20Agreement.pdf)

## Authors

- [Siddharth Mohanty](https://www.linkedin.com/in/siddharth-mohanty-6a2b77211/)

## Appendix
- Contact: neosiddharth@gmail.com
