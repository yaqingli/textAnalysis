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
        <form action="/keywords/search/" method="get">
            Category: <input name="category" type="text" value="{{category}}"/>
            <input value="Search" type="submit" />
        </form>
        <table>
            <tr>
              <th>Word</th>
              <th>Category</th>
            </tr>
            % for item in words:
                <tr>
                <td><a href="/keywords/search/?category={{item['word']}}">{{item['word']}}</a></td>
                <td>{{item['category']}}</td>
                <td>{{item['create_time']}}</td>
                </tr>
            %end

        </table>

    </body>
</html>