$(document).ready(function(){
    // Activate tooltip
    $('[data-toggle="tooltip"]').tooltip();
   
    // Select/Deselect checkboxes
    var checkbox = $('table tbody input[type="checkbox"]');
    $("#selectAll").click(function(){
        if(this.checked){
            checkbox.each(function(){
                this.checked = true;                        
            });
        } else{
            checkbox.each(function(){
                this.checked = false;                        
            });
        }
    });
 
    checkbox.click(function(){
        if(!this.checked){
            $("#selectAll").prop("checked", false);
        }
    });
 
    // Función para agregar y remover elementos de listas
    function agregarItem(IDdesde, IDhasta){
        var option = document.createElement("option");
        option.text = document.getElementById(IDdesde).value;
        document.getElementById(IDhasta).add(option);
        removerItem(IDdesde);
        selectTodos(IDhasta);
    }
 
    function removerItem(IDelemento){
        var comboBox = document.getElementById(IDelemento);
        comboBox = comboBox.options[comboBox.selectedIndex];
        // comboBox.remove();
        selectTodos(IDelemento);
    }
 
 
 
    function selectTodos(IDelemento) {
        var elementos = document.getElementById(IDelemento);
        elementos = elementos.options;
        for (var i = 0; i < elementos.length; i++) {
            elementos[i].selected = "true";
        }
    }
 
    function actualizarValorSeleccionado(combo,txtOculto) {
        var select = document.getElementById(combo);
        var valorSeleccionado = select.value;
        document.getElementById(txtOculto).value = valorSeleccionado;
    }
 
    // Asignar las funciones de agregar y borrar a los botones correspondientes
    $("#btnAgregarItem").click(function(event) {
        agregarItem('combo1','ListBox1');
        return false;
    });
 
    $("#btnBorrarItem").click(function(event) {
        removerItem('ListBox1');
        return false;
    });
 
   
    $("#btnAgregarItem2").click(function(event) {
        agregarItem('combo2','ListBox2');
        return false;
    });
 
    $("#btnBorrarItem2").click(function(event) {
        removerItem('ListBox2');
        return false;
    });
 
    $("#btnAgregarItem3").click(function(event) {
        agregarItem('combo3','ListBox3');
        return false;
    });
 
    $("#btnBorrarItem3").click(function(event) {
        removerItem('ListBox3');
        return false;
    });
 
    $("#btnAgregarItem4").click(function(event) {
        agregarItem('combo4','ListBox4');
        return false;
    });
 
    $("#btnBorrarItem4").click(function(event) {
        removerItem('ListBox4');
        return false;
    });
    //Se cambio desde aqui
    // Descargar datos como CSV
    $("#btnDescargarCSV").click(function() {
        // Obtener los datos necesarios desde la página
        var data = obtenerDatosYConvertirCSV();
    
        // Convertir los datos a formato CSV
        var csv = convertirAFormatoCSV(data);
    
        // Crear un elemento 'a' para la descarga del archivo
        var link = document.createElement('a');
        link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv));
        link.setAttribute('download', 'datos.csv');
        link.style.display = 'none';
    
        // Agregar el elemento 'a' al DOM y simular clic para descargar el archivo
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
    
    // Función para obtener los datos de la tabla y convertirlos a formato CSV
    function obtenerDatosYConvertirCSV() {
        var data = [];
        var rows = document.querySelectorAll('table tbody tr');
        rows.forEach(function(row) {
            var rowData = [];
            row.querySelectorAll('td').forEach(function(cell) {
                rowData.push(cell.textContent);
            });
            data.push(rowData.join(','));
        });
        return data.join('\n');
    }

    const scrollable = document.querySelector('.scrollable');
        let isDown = false;
        let startX;
        let scrollLeft;

        scrollable.addEventListener('mousedown', (e) => {
            isDown = true;
            scrollable.classList.add('active');
            startX = e.pageX - scrollable.offsetLeft;
            scrollLeft = scrollable.scrollLeft;
        });

        scrollable.addEventListener('mouseleave', () => {
            isDown = false;
            scrollable.classList.remove('active');
        });

        scrollable.addEventListener('mouseup', () => {
            isDown = false;
            scrollable.classList.remove('active');
        });

        scrollable.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - scrollable.offsetLeft;
            const walk = (x - startX) * 2; // ajustar la velocidad del scroll
            scrollable.scrollLeft = scrollLeft - walk;
        });
   
});