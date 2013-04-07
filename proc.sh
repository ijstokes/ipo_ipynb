for yearmon in 2012-04 2012-04 2012-05 2012-06 2012-07 2012-08 2012-09 2012-10 2012-11 2012-12 2013-01 2013-02 2013-03; do
    echo "Company Name, Symbol, Market, Price, Shares, Offer Amount, Date Priced," >  ipo-$yearmon.csv
    curl -s -o - "http://www.nasdaq.com/markets/ipos/activity.aspx?tab=pricings&month=$yearmon" |
    tr '\n' ' ' |
    sed -e "s/<div/\n<div/g;s/<\/div>/<\/div>\n/g" |
    grep -E '<div class="genTable">.*</div>' |
    perl -pe '
    s###g;
    s#,##g;
    s#\s*<tr>\s*##g;
    s#</td>#,#g;
    s#\s*<td>\s*##g;
    s#</tr>#\n#g;
    s#</a>##g;
    s#<a##g;
    s#id="[^\s"]*"##g;
    s#href="[^\s"]*"##g;
    s#</?tbody>##g;
    s#^M# #g;
    s#</?div##g;
    s#class="genTable">##g;
    s#</?table>##g;
    s#</?thead>##g;
    s#<th># #g;
    s#</th>#,#g;
    s#>##g;
    s#\\$##g;
    s#^\s*##g;
    s#,[ \t]*#,#g;
    s#[ \t]+# #g;
    ' |
    grep -v -e "Company Name" >> ipo-$yearmon.csv
done
