from flask import Flask, render_template, request, redirect, url_for, flash, flash

from models import db, User, Product, Category, Cart, Order

from app import app

@app.route('/')
def index():
    return render_template('index.html')