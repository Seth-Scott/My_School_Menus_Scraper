

# MySchoolMenus - Home Assistant Integration
Integrates school lunches from [myschoolmenus](https://myschoolmenus.com/) into your Home Assistant dashboard and automations.

## Description

MySchoolMenus does not have an accessible API. 

This application uses [Selenium](https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/firefox.html) to scrape meal data from your kid's school, saves it in a database ([MongoDB](https://www.mongodb.com/)) and publishes the data via an API ([Flask](https://flask-restful.readthedocs.io/en/latest/)). 

[Home Assistant](https://www.home-assistant.io/)'s [RESTful Sensor](https://www.home-assistant.io/integrations/sensor.rest/) can display the data on your dashboard or use it in automations. 

## Getting Started

### Dependencies

* [MongoDB](https://www.mongodb.com/)
* [Docker](https://www.docker.com/) w/ [Docker Compose](https://docs.docker.com/compose/install/)

----------------
### Installing

Installation is relatively simple, but you will need to set some environment variables in the `api` and `scraper` folders. First:
1. Clone the [repo](https://github.com/Seth-Scott/My_School_Menus_Scraper.git) 
2. create `.env.container` in the `api` folder:
    ```bash
    # touch .env.container  
    ```
    add the following to your `.env.container` file:
    ```md
    PYTHONUNBUFFERED=1
    MONGO_ROUTE=mongodb://<mongo_ip>:27017
    ```
    NOTE: Replace \<mongo-ip> with the ip address of your MongoDB instance. MongoDB is **not** preinstalled with the `compose.yaml` file.
    ******

3. create the .env.container in the `scraper` folder:
    ```bash
    # touch .env.container  
    ```
    add the following to your `.env.container` file:
    ```md
    PYTHONUNBUFFERED=1
    INSTANCE=<see_diagram>
    DISTRICT=<see_diagram>
    SCHOOL=<see_diagram>
    MENU=<see_diagram>
    MONGO_IP=<mongo_ip>
    WEBDRIVER_ADDRESS=//<host_ip>:4444/wd/hub
    ```
    NOTE: Replace above information (instance, district, etc.) with YOUR school's information. You can find it by navigating to the [myschoolmenus](https://myschoolmenus.com/) site and searching for your school, below:
    
    **DIAGRAM**
    <img title="a title" alt="Alt text" src=".\assets\scraper_env_description.png">

******
### Executing program
* Navigate into the repo's folder
* launch the program:
    ```bash
    # docker compose up
    ```
    Docker should build all of the dependencies and publish the API. Check that it's running by launching your web browser and navigating to: `http://127.0.0.1:5863/date`

* Depending on your browser's settings, you should see the current month's meals formatted as a JSON ([Firefox](https://firefox-source-docs.mozilla.org/devtools-user/json_viewer/index.html) has a built-in JSON viewer). 

* After you've verified the data is accessible, you can add a [RESTful Sensor](https://www.home-assistant.io/integrations/sensor.rest/) in Home Assistant. You'll need to edit the `configuration.yaml` wherever you have your Home Assistant instance. Add the following:: 

    ```yaml
    sensor:
    - platform: rest
        resource: http://<api_ip>:5863/date/today/
        name: "School Lunch Today"
        unique_id: "REST-API-LUNCH-01"
        payload: "{{ value_json }}"
        scan_interval: 60

    # if multiple
    - platform: rest
        resource: http://<api_ip>:5863/date/tomorrow/
        name: "School Lunch Tomorrow"
        unique_id: "REST-API-LUNCH-02"
        payload: "{{ value_json }}"
        scan_interval: 60
    ```
    * NOTE: Replace <api_ip> on both sensors with your API IP address

    * `scan_interval` is how frequently Home Assistant will poll data from API endpoints

******
### Home Assistant Automation Example
* I have an automation to narrate tomorrow's school lunch from a Google Home Mini every weekday at 7:30pm. Here is a sample of my automation, but it's likely your config will differ greatly from mine. Use this as a reference if needed:

```yaml
alias: School Lunch Narration
description: ""
trigger:
  - platform: time
    at: "19:30:00"
condition:
  - condition: time
    weekday:
      - sun
      - mon
      - tue
      - wed
      - thu
action:
  - service: media_player.volume_set
    data:
      volume_level: 0.7
    target:
      device_id: <device_id>
  - service: tts.google_translate_say
    entity_id: media_player.google_home_mini
    data_template:
      message: >-
        School lunch tomorrow is {{ states('sensor.school_lunch_tomorrow')
        }}
mode: single
```



******
## Authors

Contributors names and contact info:

[Seth Scott](https://github.com/Seth-Scott)


