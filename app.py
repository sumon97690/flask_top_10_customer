from flask import Flask, render_template
import sqlite3
import locale

app = Flask(__name__)

def get_top_customers():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # Retrieve top 10 customers based on the total value of their orders
    cursor.execute('''
        SELECT c.name, SUM(o.amount)
        FROM customers c
        INNER JOIN orders o ON c.id = o.customer_id
        WHERE o.date > date('now', '-30 days')
        GROUP BY c.id
        HAVING COUNT(o.id) = 1
        ORDER BY SUM(o.amount) DESC
        LIMIT 10
    ''')

    rows = cursor.fetchall()

    # Display the total value of each order with commas according to the Indian numbering system
    locale.setlocale(locale.LC_NUMERIC, 'en_IN')
    formatted_rows = [(row[0], locale.format_string("%d", row[1], grouping=True)) for row in rows]

    conn.close()

    return formatted_rows

@app.route('/')
def index():
    rows = get_top_customers()

    # Display the results in a table viewable from a web browser
    return render_template('index.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
