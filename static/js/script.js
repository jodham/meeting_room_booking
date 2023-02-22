$(document).ready(function() {
    var table = $('.data-table').DataTable({
        responsive: true,
    });

    var table = $('#table_id').DataTable({
        responsive: true,
    });

    var roomsTable = $('.rooms-table').DataTable({
        responsive: true,
        dom: 'Bfrtip',
        buttons: [
            {
                text: 'TRC',
                action: function ( e, dt, node, config ) {
                    dt.column(2).search( 'TRC' ).draw();
                }
            },
            {
                text: 'TOWN',
                action: function ( e, dt, node, config ) {
                    dt.column(2).search( 'TOWN' ).draw();
                }
            },
            {
                text: 'MANGU',
                action: function ( e, dt, node, config ) {
                    dt.column(2).search( 'MANGU' ).draw();
                }
            }

        ]
    });
});
