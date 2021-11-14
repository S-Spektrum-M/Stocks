# S.T.O.C.K.S.
Share Trading on Computer Knowlede Systems

## How it works
- STOCKS parses historical data to create a linear model using regression.
- The API provides two kinds of forecasts a long term(~ 6mo) and a short term(~ 2wks)
    - Long term requires 1yr of historical data.
    - short term requires 1mo of historical data.
- While github does not support rendering LaTeX The following is a LaTeX representation of
    regression:
    - $$\Large \hat{y} = r\frac{\sigma_y}{\sigma_x}(x - \overline{x}) + \overline{y} + 2\sigma_y\beta$$
    - $\hat{y}$: expected value
    - $r$: coefficent of correlation
    - $\sigma_x$: Standard Deviation of $x$
    - $\sigma_y$: Standard Deviation of $y$
    - $x$: $x$
    - $\overline{y}$: Mean value of $y$
    - $\beta$: Beta(Volatility)

## API Reference

#### Short Term Predict

```
  GET /api/long/?id={ticker}
```

| Parameter | Type     | Description                        |
|-----------|----------|------------------------------------|
| `ticker`  | `string` | **Required**. The Stock to query   |

Returns a list floating point number that represents the upper bound and lower bound for the short term.

#### Long Term Predict

```
  GET /api/long/?id={ticker}
```

| Parameter | Type     | Description                        |
|-----------|----------|------------------------------------|
| `ticker`  | `string` | **Required**. The Stock to query   |

Returns a list floating point number that represents the upper bound and lower bound for the long term.

## Acknowledgements

- [robin-stocks](https://github.com/jmfernandes/robin_stocks)
- [numpy](https://github.com/jmfernandes/robin_stocks)
- [flask](https://github.com/jmfernandes/robin_stocks)
- [Robinhood](https://robinhood.com/)

## License

- [MIT](https://choosealicense.com/licenses/mit/)
- [Robinhood Financial LLC & Robinhood Securities, LLC  Customer Agreement](https://cdn.robinhood.com/assets/robinhood/legal/Robinhood%20Customer%20Agreement.pdf)

## Authors

- [Siddharth Mohanty](https://www.linkedin.com/in/siddharth-mohanty-6a2b77211/)

## Appendix
- Contact: neosiddharth@gmail.com
