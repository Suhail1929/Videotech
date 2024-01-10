from app import app , api_url
import json
import os
import requests
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from flask_simplelogin import Message, SimpleLogin, login_required , get_username



