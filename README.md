# pp_cmd_calc_trend
Postprocessing command "calc_trend"

# Arguments
- value_col - string, columns name
- window - string, time window, example: '1M'
- time_field - keyword argument, field with time to set DateTime index, default is '_time'
`... | calc_trend column_name, '1M', time_field=time_x `

