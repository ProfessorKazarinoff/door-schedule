# TO DO
- [ ] Boarders in merged excel files
- [x] Double spaces in names converted to single spaces
- [x] Multi day course listings TuTh how to deal with them?
- [ ] Cancelled courses, leave them out of schedule 
- [x] Function to pick up ```Cancelled!``` from webpage doesn't seem to work
- [ ] If listed as STAFF, add to a separate excel sheet with a row for each section
- [ ] Get CRN from previous intr object instead of saving CRN as ```and```
- [ ] Use links to PCC Staff directory to get instructor email and phone
- [x] Get year from breadcrumbs on course page
- [ ] Get quarter from breadcrumbs on course page
- [x] Deal with times after 9pm like EET113 Summer 2018
- [x] Have separate template for day only instructors, if end time is less than 5pm, use the day schedule template

## TODO 2020Q1
- [ ] Clean out list of time_block dicts so that 2-day time blocks 'Thurs Fri' become 2 1-day time blocks 'Thurs' another time block 'Fri'
- [ ] Clean out all time block dicts so that the building name has no spaces in it.
- [ ] Convert CRN's to integers when they are read in
- [ ] Make room number a string type and allow Web to be a room number
- [ ] Make campus Web if it is a web-based class, allow campus to have 3 letters
- [ ] Make building Web it it is a web-based class, allow building to have 3 letters
- [ ] convert start_time to python datetime.time type
- [ ] convert stop_time to python datetime.time type
- [ ] auto add year as integer
- [ ] auto add quarter as integer
- [ ] fix department so that EETA and EETB don't turn up as department options
- [ ] move database creation out of models.py and into it's own function in sqllite_functions.py
