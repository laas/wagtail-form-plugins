const operators = {
    'eq': ['=', (a, b) => a === b],
    'neq': ['≠', (a, b) => a !== b],
    'lt': ['<', (a, b) => parseFloat(a) < parseFloat(b)],
    'lte': ['≤', (a, b) => parseFloat(a) <= parseFloat(b)],
    'ut': ['>', (a, b) => parseFloat(a) > parseFloat(b)],
    'ute': ['≥', (a, b) => parseFloat(a) >= parseFloat(b)],
    'in': ['∈', (a, b) => b.includes(a)],
}

function compute_visibility_condition(vc) {
    if (vc.field_id) {
        const dom_field = document.getElementById(vc.field_id)
        const [operator_str, operator_func] = operators[vc.operator]
        return {
            formula: `${ vc.field_label } ${ operator_str } "${ vc.value }"`,
            str: `"${ dom_field.value }" ${ operator_str } "${ vc.value }"`,
            result: operator_func(dom_field.value, vc.value),
        }
    }

    if (vc.and) {
        const computed_expr = vc.and.map((_vc) => compute_visibility_condition(_vc))
        return {
            formula: `(${ computed_expr.map((_vc) => _vc.formula).join(') AND (') })`,
            str: `(${ computed_expr.map((_vc) => _vc.str).join(') AND (') })`,
            result: computed_expr.every((_vc) => _vc.result),
        }
    }

    if (vc.or) {
        const computed_expr = vc.or.map((_vc) => compute_visibility_condition(_vc))
        return {
            formula: `(${ computed_expr.map((_vc) => _vc.formula).join(') OR (') })`,
            str: `(${ computed_expr.map((_vc) => _vc.str).join(') OR (') })`,
            result: computed_expr.some((_vc) => _vc.result),
        }
    }

    return {formula: '∅', str: '∅', result: true}
}

function update_fields_visibility() {
    for(const dom_field of document.querySelectorAll('input.form-control')) {
        const vc = JSON.parse(dom_field.getAttribute('data-vc'));
        const cvc = compute_visibility_condition(vc)
        console.log(`${vc.field_label}: ${ cvc.formula }  ⇒  ${ cvc.str }  ⇒  ${ cvc.result }`)

        dom_field.parentNode.style.display = cvc.result ? '' : 'none';
        // dom_field.style.backgroundColor = cvc.result ? '' : 'lightGrey';
    }
}

document.addEventListener("DOMContentLoaded", () => {
    update_fields_visibility()
    Array.from(document.querySelectorAll('input.form-control')).forEach((dom_input) => {
        dom_input.addEventListener('change', () => update_fields_visibility())
    });
});
