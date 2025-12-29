import sqlite3
from pathlib import Path
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash

from helpers import analyze_code

BASE_DIR = Path(__file__).resolve().parent
