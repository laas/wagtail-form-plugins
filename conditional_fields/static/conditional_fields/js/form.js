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
    if (rule.entry) {
        const dom_field = document.getElementById(rule.entry.target)
        const [opr_str, opr_func] = OPERATORS[rule.entry.opr]
        return {
            formula: `${ dom_field.labels[0].innerText } ${ opr_str } "${ rule.entry.val }"`,
            str: `"${ dom_field.value }" ${ opr_str } "${ rule.entry.val }"`,
            result: opr_func(dom_field.value, rule.entry.val),
        }
    }

    if (rule.and) {
        const computed_rules = rule.and.map((_rule) => compute_rule(_rule))
        return {
            formula: `(${ computed_rules.map((_rule) => _rule.formula).join(') AND (') })`,
            str: `(${ computed_rules.map((_rule) => _rule.str).join(') AND (') })`,
            result: computed_rules.every((_rule) => _rule.result),
        }
    }

    if (rule.or) {
        const computed_rules = rule.or.map((_rule) => compute_rule(_rule))
        return {
            formula: `(${ computed_rules.map((_rule) => _rule.formula).join(') OR (') })`,
            str: `(${ computed_rules.map((_rule) => _rule.str).join(') OR (') })`,
            result: computed_rules.some((_rule) => _rule.result),
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
    for(const dom_field of document.querySelectorAll('form > p > input.form-control')) {
        const label = dom_field.labels[0].innerText
        const rule = JSON.parse(dom_field.getAttribute('data-rule'))
        const cmp_rule = compute_rule(rule)
        console.log(`${label}: ${ cmp_rule.formula }  ⇒  ${ cmp_rule.str }  ⇒  ${ cmp_rule.result }`)

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
