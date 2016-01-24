$.tablesorter.addParser({
    id: 'monthYear',
    is: function(s) {
        return false;
    },
    format: function(s) {
        // remove extra spacing
        s = $.trim(s.replace(/\s+/g, ' '));
        // process date
        var date = s.match(/^(\w{3})[ ](\d{4})$/),
        m = date ? date[1] + ' 1 ' || '' : '',
        y = date && date[2] ? date[2] || '' : '';
        return new Date(m + y).getTime() || '';
    },
    type: 'Numeric'
});

$(document).ready(function() 
{ 
    $("#myTable").tablesorter({
        headers: {
            1: {
                sorter: 'monthYear'
            }
        }
    }); 
        } 
    ); 