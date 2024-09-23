const OPERATORS = {
    'eq': ['=', (a, b) => a === b],
    'neq': ['≠', (a, b) => a !== b],
    'lt': ['<', (a, b) => parseFloat(a) < parseFloat(b)],
    'lte': ['≤', (a, b) => parseFloat(a) <= parseFloat(b)],
    'ut': ['>', (a, b) => parseFloat(a) > parseFloat(b)],
    'ute': ['≥', (a, b) => parseFloat(a) >= parseFloat(b)],
    'in': ['∈', (a, b) => b.includes(a)],
    'nin': ['∉', (a, b) => ! b.includes(a)],
    'c': ['✔', (a, b) => a],
    'nc': ['✖', (a, b) => !a],
}
const DEBOUNCE_DELAY = 300;


function compute_rule(rule) {
    if (rule.field_id) {
        const dom_field = document.getElementById(rule.field_id)
        const [operator_str, operator_func] = operators[rule.operator]
        return {
            formula: `${ rule.field_label } ${ operator_str } "${ rule.value }"`,
            str: `"${ dom_field.value }" ${ operator_str } "${ rule.value }"`,
            result: operator_func(dom_field.value, rule.value),
        }
    }

    if (rule.and) {
        const computed_expr = rule.and.map((_rule) => compute_rule(_rule))
        return {
            formula: `(${ computed_expr.map((_rule) => _rule.formula).join(') AND (') })`,
            str: `(${ computed_expr.map((_rule) => _rule.str).join(') AND (') })`,
            result: computed_expr.every((_rule) => _rule.result),
        }
    }

    if (rule.or) {
        const computed_expr = rule.or.map((_rule) => compute_rule(_rule))
        return {
            formula: `(${ computed_expr.map((_rule) => _rule.formula).join(') OR (') })`,
            str: `(${ computed_expr.map((_rule) => _rule.str).join(') OR (') })`,
            result: computed_expr.some((_rule) => _rule.result),
        }
    }

    return {formula: '∅', str: '∅', result: true}
}

function debounce(callback) {
    let timer;
    return () => {
        clearTimeout(timer);
        timer = setTimeout(() => callback(), DEBOUNCE_DELAY);
    }
}

function update_fields_visibility() {
    for(const dom_field of document.querySelectorAll('input.form-control')) {
        const rule = JSON.parse(dom_field.getAttribute('data-rule'));
        const cmp_rule = compute_rule(rule)
        console.log(`${rule.field_label}: ${ cmp_rule.formula }  ⇒  ${ cmp_rule.str }  ⇒  ${ cmp_rule.result }`)

        dom_field.parentNode.style.display = cmp_rule.result ? '' : 'none';
        // dom_field.style.backgroundColor = cmp_rule.result ? '' : 'lightGrey';
    }
}

document.addEventListener("DOMContentLoaded", () => {
    update_fields_visibility()
    Array.from(document.querySelectorAll('input.form-control')).forEach((dom_input) => {
        dom_input.addEventListener('input', debounce(() => update_fields_visibility()))
    });
});
