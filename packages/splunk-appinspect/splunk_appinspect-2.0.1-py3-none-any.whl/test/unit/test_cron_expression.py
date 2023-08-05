# Copyright 2016 Splunk Inc. All rights reserved.

# Python Standard Libraries
import pytest
from splunk_appinspect.cron_expression import CronExpression


def test_all_wildcards_should_be_high_occurring():
    exp = CronExpression('* * * * *')
    assert exp.is_high_occurring()


def test_4_minutes_step_should_be_high_occurring():
    exp = CronExpression('*/4 * * * *')
    assert exp.is_high_occurring()


def test_5_minutes_step_should_not_be_high_occurring():
    exp = CronExpression('*/5 * * * *')
    assert not exp.is_high_occurring()


def test_over_12_separated_values_should_be_high_occurring():
    exp = CronExpression('1,2,3,4,5,6,7,8,9,10,11,12,13 * * * *')
    assert exp.is_high_occurring()


def test_less_than_or_equal_to_12_separated_values_should_not_be_high_occurring():
    exp = CronExpression('1,2,3,4,5,6,7,8,9,10,11,12 * * * *')
    assert not exp.is_high_occurring()


def test_short_range_value_should_not_be_high_occurring():
    exp = CronExpression('1-10 * * * *')
    assert not exp.is_high_occurring()


def test_long_range_value_should_be_high_occurring():
    exp = CronExpression('1-40 * * * *')
    assert exp.is_high_occurring()


def test_multiple_short_ranges_value_should_be_high_occurring():
    exp = CronExpression('1-10,20-30 * * * *')
    assert exp.is_high_occurring()


def test_overlapped_short_ranges_value_should_not_be_high_occurring():
    exp = CronExpression('5-10,2-13 * * * *')
    assert not exp.is_high_occurring()


def test_short_ranges_value_with_step_value_should_not_be_high_occurring():
    exp = CronExpression('1-10,*/40 * * * *')
    assert not exp.is_high_occurring()

def test_short_ranges_and_intervals_with_step_value_should_not_be_high_occurring():
    exp = CronExpression('1-20/4 * * * *')
    assert not exp.is_high_occurring()

def test_step_value_with_multiple_separated_values_should_be_high_occurring():
    exp = CronExpression('*/10,1,2,3,4,5,6,7 * * * *')
    assert exp.is_high_occurring()


def test_minute_field_with_characters_should_be_invalid():
    exp = CronExpression('abc * * * *')
    with pytest.raises(ValueError):
        exp.is_high_occurring()
    assert not exp.is_valid()


def test_larger_than_59_minute_value_should_be_invalid():
    exp = CronExpression('61 * * * *')
    with pytest.raises(Exception):
        exp.is_high_occurring()
    assert not exp.is_valid()


def test_minus_minute_value_should_be_invalid():
    exp = CronExpression('-1 * * * *')
    with pytest.raises(Exception):
        exp.is_high_occurring()
    assert not exp.is_valid()


def test_non_high_occurring_step_value_with_high_occurring_hours_value_should_not_be_high_occurring():
    exp = CronExpression('*/10 */4 * * *')
    assert not exp.is_high_occurring()


def test_non_high_occurring_range_value_with_high_occurring_hours_value_should_not_be_high_occurring():
    exp = CronExpression('10-15 */4 * * *')
    assert not exp.is_high_occurring()


def test_separated_with_multiple_whitespaces_should_be_valid():
    exp = CronExpression('10 *  *   * * ')
    assert exp.is_valid()


def test_four_asterisks_should_be_invalid():
    exp = CronExpression('* * * *')
    _ = exp.is_high_occurring()
    assert not exp.is_valid()


def test_six_asterisks_should_be_invalid():
    exp = CronExpression('* * * * * *')
    _ = exp.is_high_occurring()
    assert not exp.is_valid()
