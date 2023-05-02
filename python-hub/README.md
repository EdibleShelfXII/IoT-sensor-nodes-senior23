## API:

### /data/all
    Displays temperature and relative humidity for all sensor nodes in  a JSON format:
    
        [{"adr":"0","msg_id":"0","t_ms":"0","key_t_ms":"0","t_ls":"0","key_t_ls":"0","rh_ms":"0","key_rh_ms":"0","rh_ls":"0","key_rh_ls":"0","temperature":"10","relative_humidity":"0","date_time":"yyyy-MM-ddThh:mm:ss"}, 
        {"adr":"1","msg_id":"0","t_ms":"0","key_t_ms":"0","t_ls":"0","key_t_ls":"0","rh_ms":"0","key_rh_ms":"0","rh_ls":"0","key_rh_ls":"0","temperature":"10","relative_humidity":"0","date_time":"yyyy-MM-ddThh:mm:ss"}, 
        ...       
        {"adr":"7","msg_id":"0","t_ms":"0","key_t_ms":"0","t_ls":"0","key_t_ls":"0","rh_ms":"0","key_rh_ms":"0","rh_ls":"0","key_rh_ls":"0","temperature":"10","relative_humidity":"0","date_time":"yyyy-MM-ddThh:mm:ss"}]
    
### /data/0 ... /data/7
    Displays temperature and relative humidity for indicated sensor node in format:
    
        {"adr":"7","msg_id":"0","t_ms":"0","key_t_ms":"0","t_ls":"0","key_t_ls":"0","rh_ms":"0","key_rh_ms":"0","rh_ls":"0","key_rh_ls":"0","temperature":"10","relative_humidity":"0","date_time":"yyyy-MM-ddThh:mm:ss"}
