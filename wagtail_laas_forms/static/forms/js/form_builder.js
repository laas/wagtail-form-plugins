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

const FIELD_CUSTOMIZATION = {
    'singleline': ['char'],
    'multiline': ['char'],
    'email': ['char'],
    'number': ['number'],
    'url': ['char'],
    'checkbox': ['none'],
    'checkboxes': ['dropdown'],
    'dropdown': ['dropdown'],
    'multiselect': ['dropdown'],
    'radio': ['dropdown'],
    'date': ['date'],
    'datetime': ['date'],
    'hidden': ['char'],
}


function get_fields() {
    const dom_form_fields = document.querySelector('.formbuilder-fields-block > div[data-streamfield-stream-container]')
    const dom_block_fields = dom_form_fields.querySelectorAll(':scope > [data-contentpath]:not([aria-hidden])');

    return Object.fromEntries(Array.from(dom_block_fields).map((dom_block, index) => [
        dom_block.getAttribute('data-contentpath'),
        {
            'index': index,
            'contentpath': dom_block.getAttribute('data-contentpath'),
            'label': dom_block.querySelector('.formbuilder-field-block-label input').value || `field n°${ index + 1}`,
            'dom_block': dom_block,
            'type': dom_block.getElementsByClassName('formbuilder-field-block')[0].className.replace('formbuilder-field-block', '').split('-')[1]
        }
    ]));
}

function fill_dropdown(dom_dropdown, choices) {
    dom_dropdown.innerHTML = "";

    for (const [choice_key, choice_label, disabled] of choices) {
        const option = document.createElement('option');
        option.value = choice_key;
        option.text = choice_label;
        option.disabled = disabled;
        dom_dropdown.appendChild(option);    
    }
}


class BEBBlockDefinition extends window.wagtailStreamField.blocks.StructBlockDefinition {
    get_rule_subjects_choices() {
        const fields_choices = Object.values(this.fields)
            .filter((f) => this.current_field.index > f.index)
            .map(f => [f.contentpath, f.label, false])

        return [
            ['', 'Fields:', true],
            ...fields_choices,
            ['', 'Expression:', true],
            ['or', 'one of...', false],
            ['and', 'all of...', false],
        ]
    }

    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(placeholder, prefix, initialState, initialError);
        this.dom_struct_block = block.container[0];

        if (this.dom_struct_block.closest('[data-contentpath="rules"] > div.formbuilder-block-hidden') !== null) {
            return block
        }

        this.dom_rule_block = block.container[0].closest('[data-contentpath="rule"]')
        this.dom_field_block = this.dom_rule_block.closest('.formbuilder-field-block');
        this.dom_field_block_container = this.dom_field_block.parentNode.parentNode.parentNode;

        this.fields = get_fields()
        this.current_field = this.fields[this.dom_field_block_container.getAttribute('data-contentpath')];

        if (this.current_field.index === 0) {
            this.dom_rule_block.style.display = 'none'
            return block;
        }

        const dom_rule_subject_dropdown = this.dom_rule_block.querySelector('[data-contentpath="field"] select')
        fill_dropdown(dom_rule_subject_dropdown, this.get_rule_subjects_choices())

        return block;
    }
}
window.telepath.register('forms.blocks.BooleanExpressionBuilderBlock', BEBBlockDefinition);
