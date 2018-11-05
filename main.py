#!/usr/bin/env python3
# Copyright (c) 2018 Jeff Lund, Kevin Young
import Reviews
import config

"""
Runs app factory to create Movie Review app.
"""
app = Reviews.create_app(config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
 
