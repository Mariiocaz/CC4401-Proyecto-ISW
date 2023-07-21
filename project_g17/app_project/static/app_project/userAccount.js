let dataTable;
let dataTableIsInitialized = false;

let fechaInicio = document.getElementById("fecha-inicio");
let fechaTermino = document.getElementById("fecha-termino");
let categoriaFiltro = document.getElementById("categoria-filtro");

window.addEventListener('load', () => {
  let dateInputs = document.querySelectorAll('input[type="date"]');
  let selectElements = document.querySelectorAll('select');

  dateInputs.forEach((input) => {
    input.value = '';
  });

  selectElements.forEach((select) => {
    select.selectedIndex = 0;
  });
});

// Ahora hago un fetch usando AJAX para no tener que recargar la página al hacer submit
document.getElementById("output-form-3").addEventListener('submit', (event) => {

  event.preventDefault();
  let formData = new FormData(event.target);

  fetch('/modify_transaccion/', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': '{{ csrf_token }}'
    }
  })
  .then(response => response.text())
  .then(data => {
    let saldo = document.getElementById("saldo");
    let error_mod = document.getElementById("error-modificacion");
    let error_trans = document.getElementById("error-transaccion");
    let error_cat = document.getElementById("error-categoria");
    data = JSON.parse(data);
    saldo.innerHTML = `Saldo: $${data.saldo}`;
    error_mod.innerHTML = `${data.error}`;
    error_cat.innerHTML = "";
    error_trans.innerHTML = "";
  })
  let modal = document.getElementById("myModal");
  
  modal.style.display = "none";
  initDataTable();
  

});

const dataTableOptions = {
    responsive: true,
    rowReorder: {
      selector: 'td:nth-child(0)'
    },
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5] },
        { orderable: false, targets: [1,3,4,5] },
        { searchable: false, targets: [2, 3, 4,5] },
        { responsivePriority: 1, targets: 5 }
    ],
    pageLength: 4,
    destroy: true
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    // ahora hago que listTransacciones() me retorne las categorias que envie desde la view, para despues usarlas en modify
    let categorias = await listTransacciones();

    dataTable = $("#datatable-transacciones").DataTable(dataTableOptions);

    dataTableIsInitialized = true;

    modify(categorias);
    

};

const listTransacciones = async () => {
    try {
        const response = await fetch(`/list_transacciones/?categoria-filtro=${categoriaFiltro.value}&fecha-inicio=${encodeURIComponent(fechaInicio.value)}&fecha-fin=${encodeURIComponent(fechaTermino.value)}`);
        const data = await response.json();
        let content = ``;
        data.transacciones.forEach((transaccion, index) => {
            let rowClass = "<tr>";
            if (transaccion.monto < 0) {
              rowClass = "<tr class=fondoRojo>";
            }
            content += `
                ${rowClass}
                    <td>${index + 1}</td>
                    <td>${transaccion.titulo}</td>
                    <td>${transaccion.monto}</td>
                    <td>${transaccion.fecha_creacion}</td>
                    <td>${transaccion.categoria_id}</td>
                    <td>
                        <button class='btn btn-sm btn-primary' id='${transaccion.id}'><i class='fa-solid fa-pencil'></i></button>
                        <button class='btn btn-sm btn-danger' id='${transaccion.id}'><i class='fa-solid fa-trash-can'></i></button>
                    </td>
                </tr>`;
        });
        tableBody_transacciones.innerHTML = content;
        return data.categorias;
    } catch (ex) {
        alert(ex);
    }
};

async function delete_from_table(id) {
    let modal_delete = document.getElementById("myDeleteModal");
    modal_delete.style.display = "none";
    const response = await fetch('/delete_transaccion/?id='+id);
    let saldo = document.getElementById("saldo");
    const data = await response.json()
    let nuevoSaldo = data.saldoFinal
    saldo.innerHTML = `Saldo: $${nuevoSaldo}`;
    initDataTable();
    
}
window.addEventListener("load", async () => {
    await initDataTable();
});

const modify = (categorias) => {
  let table = document.getElementById("datatable-transacciones");
  // Get the modal
  let modal = document.getElementById("myModal");
  let modal_delete = document.getElementById("myDeleteModal");
  // Get the <span> element that closes the modal
  let span = document.getElementsByClassName("x")[0];
  let span2 = document.getElementsByClassName("x")[1];

  // Seteo el span para que permita salir del modal con la 'X'
  span.onclick = () => {
    modal.style.display = "none";
  }

  span2.onclick = () => {
    modal_delete.style.display = "none";
  }

  // Tambien se puede cerrar el modal haciendo click fuera de este
  window.onclick = (event) => {
    if (event.target == modal || event.target == modal_delete) {
      modal.style.display = "none";
      modal_delete.style.display = "none";
    }
  }
  for (let i = 1; i < table.rows.length; i++) {
    const row = table.rows[i];
    const rowName = row.cells[1].innerHTML;
    const rowAmount = row.cells[2].innerHTML;
    const rowDate = row.cells[3].innerHTML;
    const rowCategory = row.cells[4].innerHTML;
    const buttons = row.cells[5];
    const modifyButton = buttons.firstChild.nextSibling;
    const deleteButton = buttons.firstChild.nextSibling.nextSibling.nextSibling;
    const id = modifyButton.id;

    
    
    modifyButton.addEventListener("click", () => {
      try {
        let cat = "";
        categorias.forEach((categoria) => {
          if (categoria.nombre != rowCategory) {
            cat += `<option class="form-group" value="${categoria.nombre}" name="${categoria.nombre}">${categoria.nombre}</option>\n`;
          }
          else {
            cat += `<option class="form-group" selected="selected" value="${categoria.nombre}" name="${categoria.nombre}">${categoria.nombre}</option>\n`;
          }
        });
        modal.style.display = "block";
        $(modal).find('#modal-input').html(`
        <div class="form-group">
          <h2>Modificar ${rowName}</h2>
          <input type="hidden" name="idMod" value="${id}">
        </div>
        <div class="form-group">
          <label for="nameMod">Nombre (Nombre actual: ${rowName})</label>
          <input type="text" class="form-control" value="${rowName}" placeholder="Ingresa un nombre" name="nameMod" size="50">
        </div>
        <div class="form-group">
          <label for="amountMod">Monto (Monto actual: ${rowAmount})</label>
          <input type="text" class="form-control" value="${rowAmount}" placeholder="Ingresa un monto" name="amountMod" size="50">
        </div>
        <div class="form-group">
          <label for="class">Fecha (Fecha actual: ${rowDate})</label>
          <input type="date" class="form-control" value="${rowDate}" name="dateMod">
        </div>
        <div class="form-group">
          <label for="classMod">Categoría (Categoría actual: ${rowCategory})</label>
          <select class="form-group" name="classMod"  id="nombre">
            <option class="disabled" value="">Elige una categoría</option>
                      ${cat}
          </select>
        </div>

        
        `); // Uso JQuery, si no tira error
      }

      catch (ex) {
        alert(ex);
      }

    });

    deleteButton.addEventListener("click", () => {
      
      try {
        modal_delete.style.display = "block";
        $(modal_delete).find('#modal-delete').html(`
        <div class="form-group">
        <h2>¿Está seguro de borrar tu transacción ${rowName}? Esta acción no se puede deshacer</h2>
        <button class='btn btn-sm btn-danger'onclick="delete_from_table(${id})">Borrar</button>
        </div>
        `); // Uso JQuery, si no tira error
      }

      catch (ex) {
        alert(ex);
      }

    });
    
    
  }    
}
/* Boton para resetear filtros*/
const resetFiltersBtn = document.getElementById("reset-filters-btn");

resetFiltersBtn.addEventListener("click", function() {
  // Restablecer los valores de los campos de fecha
  document.getElementById("fecha-inicio").value = "";
  document.getElementById("fecha-termino").value = "";

  // Restablecer el valor del campo de categoría
  document.getElementById("categoria-filtro").selectedIndex = 0;
  initDataTable();
});

categoriaFiltro.addEventListener("change", initDataTable);
fechaInicio.addEventListener("input", initDataTable);
fechaTermino.addEventListener("input", initDataTable);
