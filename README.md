# S.T.O.C.K.S.
Share Trading on Computer Knowlede Systems

## How it works
- STOCKS parses historical data to create a linear model using regression.
- The API provides two kinds of forecasts a long term(~ 6mo) and a short term(~ 2wks)
    - Long term requires 1yr of historical data.
    - short term requires 1mo of historical data.
- While github does not support rendering LaTeX The following is a LaTeX representation of
    regression: $$\Large \hat{y} = r\frac{\sigma_y}{\sigma_x}(x - \overline{x}) + \overline{y}$$

## API Reference

#### Short Term Predict

```
  GET /api/short/items${ticker}
```

| Parameter | Type     | Description                        |
| :-------- | :------- | :-------------------------------   |
| `ticker`  | `string` | **Required**. The Stock to query   |

Returns a floating point number calculated by the backend.

#### Long Term Predict

```
  GET /api/long/items${ticker}
```

| Parameter | Type      | Description                        |
| --------  | -------   | -------------------------------    |
| `ticker`  | `string`  | **Required**. The Stock to query   |

Returns a floating point number calculated by the backend.

## Acknowledgements

- [robin-stocks](https://github.com/jmfernandes/robin_stocks)
- [Robinhood](https://robinhood.com/)

## License

- [MIT](https://choosealicense.com/licenses/mit/)
- [Robinhood Financial LLC & Robinhood Securities, LLC  Customer Agreement](https://cdn.robinhood.com/assets/robinhood/legal/Robinhood%20Customer%20Agreement.pdfhttps://cdn.robinhood.com/assets/robinhood/legal/Robinhood%20Customer%20Agreement.pdf)

## Authors

- [Siddharth Mohanty](https://www.linkedin.com/in/siddharth-mohanty-6a2b77211/)

## Appendix
- Contact: neosiddharth@gmail.com
