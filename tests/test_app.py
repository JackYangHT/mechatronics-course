
import asyncio
import pytest
from pyppeteer import launch

@pytest.mark.asyncio
async def test_page_loads_and_has_title():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://127.0.0.1:5000/')
    title = await page.title()
    await browser.close()
    assert "MIT-Inspired Mechatronics Course (G7-G12)" in title

@pytest.mark.asyncio
async def test_header_and_language_buttons():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://127.0.0.1:5000/')
    header = await page.querySelector('h1')
    header_text = await page.evaluate('(element) => element.textContent', header)
    assert "Mechatronics: G7 Foundations" in header_text

    buttons = await page.querySelectorAll('.flag-button')
    assert len(buttons) == 3 # en, th, zh

    await browser.close()

@pytest.mark.asyncio
async def test_language_switching():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://127.0.0.1:5000/')
    
    # Switch to Thai
    await page.click('button[title="Thai"]')
    await page.waitForSelector('#language-display')
    lang_display = await page.evaluate('document.getElementById("language-display").textContent')
    assert "Language: TH" in lang_display

    # Check if a unit title is in Thai
    unit_title = await page.evaluate('document.querySelector(".course-card p").textContent')
    assert "G7 หน่วยที่ 1" in unit_title

    await browser.close()

@pytest.mark.asyncio
async def test_unit_locking_and_unlocking():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://127.0.0.1:5000/')

    # Initially, later units are locked
    locked_units = await page.querySelectorAll('.locked-unit')
    assert len(locked_units) > 0

    # Select the first unit
    await page.click('.unlocked-card')
    
    # Answer the quiz correctly
    await page.waitForSelector('#quiz-area')
    
    # Question 1, Option 3 (Lever)
    await page.click('input[name="quiz-q0"][value="2"]')
    
    # Question 2, Option 3 (Transfer and change speed/torque)
    await page.click('input[name="quiz-q1"][value="2"]')

    await page.click('#submit-quiz-btn')
    
    # Check for success message
    await page.waitForSelector('#quiz-feedback')
    feedback = await page.evaluate('document.getElementById("quiz-feedback").textContent')
    assert "PERFECT" in feedback

    # Wait for dashboard to re-render
    await asyncio.sleep(2) 

    # Now, the next unit should be unlocked. 
    # This is a simplification. A more robust test would check for a specific unit.
    unlocked_cards = await page.querySelectorAll('.unlocked-card')
    assert len(unlocked_cards) >= 2 # At least G7_U1 and G7_U2 should be unlocked

    await browser.close()

