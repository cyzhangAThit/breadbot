# Bread Bot

## Overview
* Bread Bot is a pure-Python, pure-text chatterbot. The aim is to build a fast speed, short text message QA system.
  * Why Python: For platform independence and fast development.
  * Why text only: Text can express anything, easily to be processed, fast to be translated. That's why we only use text message for Bread Bot.

## Setup
* Install
  * Make sure you have installed mongodb
  * sudo python3 setup.py install
* Uninstall
  * sudo python3 setup.py uninstall
* Clean (not uninstall)
  * sudo python3 setup.py clean

## How to use
* Run command "breadbot"
* Then u can talk with bread:
  * Type "help" for simple & quick help.
  * Or, Type "readme" to display this web page.
* Useful chatting:
  * Search Baidu: type "d xxx".
  * Search Wikipedia: type "w xxx".
  * Search dictionary: type "s xxx". (Need install sdcv first)
  * Teach dialogues: type "t question; answer" (Use ";" to split question and answer)
  * If return message is too long, type "n" will turn to next page.
  * Generally, Bread return the dia data result, But when you type the same words twice, Bread will return the klg data result.

## Surpported Platform
* WeChat Official Account
  * How to connect: Write your token and ip on /etc/bread.cfg, then run command "breadbot start", it will soon connect to WeChat Official Account (https://mp.weixin.qq.com) and start working.

## Seek more
* Author: Mark Young
* Email: ideamark@qq.com
