<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }

        th, td {
            text-align: left;
            padding: 8px;
        }

        tr:nth-child(even){background-color: #f2f2f2}
        </style>
    </head>
    <body>
        <form action="/keywords/addword" method="post">
            Word: <input name="word" type="text" />
            Category: <input name="category" type="text" />
            <input value="Add" type="submit" />
        </form>
        <table>
            <tr>
              <th>Word</th>
              <th>Category</th>
            </tr>
            % for item in words:
        </table>

    </body>
</html>