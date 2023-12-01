document.addEventListener('DOMContentLoaded', function() {

const seleccion = document.getElementById('seleccion');
const formulario1 = document.getElementById('decreto_27');
const formulario2 = document.getElementById('decreto_255');

seleccion.addEventListener('change', function() {
    formulario1.style.display = 'none';
    formulario2.style.display = 'none';

    const opcionSeleccionada = seleccion.value;
    if (opcionSeleccionada === 'decreto_27') {
        formulario1.style.display = 'block';
    } else if (opcionSeleccionada === 'decreto_255') {
        formulario2.style.display = 'block';
    }
});

const a = document.querySelectorAll('input[type="checkbox"][name="a"]');
const b = document.querySelectorAll('input[type="checkbox"][name="b"]');
const c = document.querySelectorAll('input[type="checkbox"][name="c"]');
const d = document.querySelectorAll('input[type="checkbox"][name="d"]');
const e = document.querySelectorAll('input[type="checkbox"][name="e"]');
const f = document.querySelectorAll('input[type="checkbox"][name="f"]');
const g = document.querySelectorAll('input[type="checkbox"][name="g"]');
const h = document.querySelectorAll('input[type="checkbox"][name="h"]');
const i = document.querySelectorAll('input[type="checkbox"][name="i"]');
const j = document.querySelectorAll('input[type="checkbox"][name="j"]');
const k = document.querySelectorAll('input[type="checkbox"][name="k"]');
const l = document.querySelectorAll('input[type="checkbox"][name="l"]');
const m = document.querySelectorAll('input[type="checkbox"][name="m"]');
const n = document.querySelectorAll('input[type="checkbox"][name="n"]');

a.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        a.forEach(otherCheckbox => {
            if (otherCheckbox !== checkbox) {
                otherCheckbox.checked = false;
            }
        });
    });
});

b.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        b.forEach(otherCheckbox => {
            if (otherCheckbox !== checkbox) {
                otherCheckbox.checked = false;
            }
        });
    });
});

c.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        c.forEach(otherCheckbox => {
            if (otherCheckbox !== checkbox) {
                otherCheckbox.checked = false;
            }
        });
    });
});

d.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        d.forEach(otherCheckbox => {
            if (otherCheckbox !== checkbox) {
                otherCheckbox.checked = false;
            }
        });
    });
});

e.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        e.forEach(otherCheckbox => {
            if (otherCheckbox !== checkbox) {
                otherCheckbox.checked = false;
            }
        });
    });
});

f.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        f.forEach(otherCheckbox => {
            if (otherCheckbox !== checkbox) {
                otherCheckbox.checked = false;
            }
        });
    });
});

g.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        g.forEach(otherCheckbox => {
            if (otherCheckbox !== checkbox) {
                otherCheckbox.checked = false;
            }
        });
    });
});

h.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        h.forEach(otherCheckbox => {
            if (otherCheckbox !== checkbox) {
                otherCheckbox.checked = false;
            }
        });
    });
});

i.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        i.forEach(otherCheckbox => {
            if (otherCheckbox !== checkbox) {
                otherCheckbox.checked = false;
            }
        });
    });
});

j.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        j.forEach(otherCheckbox => {
            if (otherCheckbox !== checkbox) {
                otherCheckbox.checked = false;
            }
        });
    });
});

k.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        k.forEach(otherCheckbox => {
            if (otherCheckbox !== checkbox) {
                otherCheckbox.checked = false;
            }
        });
    });
});

l.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        l.forEach(otherCheckbox => {
            if (otherCheckbox !== checkbox) {
                otherCheckbox.checked = false;
            }
        });
    });
});

m.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        m.forEach(otherCheckbox => {
            if (otherCheckbox !== checkbox) {
                otherCheckbox.checked = false;
            }
        });
    });
});

n.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        n.forEach(otherCheckbox => {
            if (otherCheckbox !== checkbox) {
                otherCheckbox.checked = false;
            }
        });
    });
});

});