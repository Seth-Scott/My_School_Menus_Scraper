**Database to API**


A simple flask API server to integrate data from MongoDB into Home Assistant


Prerequisites:
* MSM School Menu Scraper (add GitHub URL)
* MongoDB
* Home Assistant


Add the following to your `configuration.yaml` file:

```yaml
sensor:
  - platform: rest
    resource: http://192.168.0.X:XXXX/date/today/
    name: "School Lunch Today"
    unique_id: "REST-API-LUNCH-01"
    payload: "{{ value_json }}"
    scan_interval: 60

  # if multiple
  - platform: rest
    resource: http://192.168.0.X:XXXX/date/tomorrow/
    name: "School Lunch Tomorrow"
    unique_id: "REST-API-LUNCH-02"
    payload: "{{ value_json }}"
    scan_interval: 60
```

* `scan_interval` is how frequently Home Assistant will get data from API endpoints