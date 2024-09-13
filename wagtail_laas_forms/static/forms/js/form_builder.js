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
const MAX_TITLE_LENGTH = 90

function update_vc_heading(dom_vc) {
    setTimeout(() => {
        const dom_block = dom_vc.querySelector('div.w-panel__content').firstElementChild
        const dom_heading = dom_vc.querySelector('h2.w-panel__heading')
        const dom_type = dom_heading.querySelector('span.c-sf-block__type')
        const dom_title = dom_heading.querySelector('span.c-sf-block__title')

        if (dom_block.classList.contains('formbuilder-condition-block')) {
            const dom_field_label = dom_block.querySelector('[data-contentpath="field_label"] input')
            const dom_operator = dom_block.querySelector('[data-contentpath="operator"] select')
            const dom_value = dom_block.querySelector('[data-contentpath="value"] input')

            dom_title.innerText = `${ dom_field_label.value } ${ OPERATORS[dom_operator.value][0] } "${ dom_value.value }"`
            dom_type.innerText = dom_title.innerText
        } else if (dom_block.classList.contains('formbuilder-boolean-expression-block')) {
            const dom_titles = dom_block.querySelectorAll(':scope > div > [data-contentpath]:not([aria-hidden]) > section > div > h2.w-panel__heading span.c-sf-block__title')
            str_title = Array.from(dom_titles).map((dom_title) => `(${ dom_title.innerText })`).join(` ${ dom_type.innerText } `)
            dom_title.innerText = str_title.length > MAX_TITLE_LENGTH ? str_title.substring(0, MAX_TITLE_LENGTH) + '...' : str_title
        }
    }, 10)
}

function get_fields() {
    const dom_form_fields = document.querySelector('[data-contentpath="form_fields"] [data-streamfield-stream-container]')
    const dom_block_fields = dom_form_fields.querySelectorAll(':scope > [data-contentpath]:not([aria-hidden])');
    
    return Array.from(dom_block_fields).map((field_dom, index) => ({
        'index': index,
        'contentpath': field_dom.getAttribute('data-contentpath'),
        'label': field_dom.querySelector('[data-contentpath="label"] input').value || `field n°${ index + 1}`,
        'dom': field_dom,
        'type': field_dom.getElementsByClassName('formbuilder-field-block')[0].className.replace('formbuilder-field-block', '').split('-')[1]
    }))
}

class FormFieldBlockDefinition extends window.wagtailStreamField.blocks.StructBlockDefinition {
    on_add_condition(dom_tooltip) {
        const fields = get_fields();
        const dom_current_field = dom_tooltip.closest('.formbuilder-field-block').parentNode.parentNode.parentNode;
        const current_field = fields.find((field) => field.dom.getAttribute('data-contentpath') === dom_current_field.getAttribute('data-contentpath'))
        const dom_field_choices_group = dom_tooltip.querySelector('.w-combobox__optgroup')
        const dom_field_choices = dom_field_choices_group.getElementsByClassName('w-combobox__option')

        dom_field_choices_group.classList.add('formbuilder-field-choices-group')

        for (const [choice_index, dom_field_choice] of Array.from(dom_field_choices).entries()) {
            dom_field_choice.classList.remove('w-combobox__option--col1', 'w-combobox__option--col2')
            if (choice_index < fields.length) {
                dom_field_choice.classList.add('formbuilder-field-choice', `w-combobox__option--col${ choice_index % 2 + 1 }`)
                dom_field_choice.querySelector('.w-combobox__option-text').innerText = fields[choice_index].label
                dom_field_choice.setAttribute('disabled', choice_index >= current_field.index);
                dom_field_choice.addEventListener("click", () => window.form_builder_selected_choice = fields[choice_index]);
            }
        }
    }

    on_label_change(dom_block, dom_label) {
        const dom_vcs = document.querySelectorAll('.formbuilder-boolean-expression-block > div > [data-contentpath]:not([aria-hidden])');

        Array.from(dom_vcs).map((dom_vc) => {
            const dom_field_id = dom_vc.querySelector('[data-contentpath="field_id"] input')
            if (dom_block.getAttribute('data-contentpath') === dom_field_id?.value) {
                const dom_field_label = dom_vc.querySelector('[data-contentpath="field_label"] input')
                dom_field_label.value = dom_label.value
                update_vc_heading(dom_vc)
            }
        });
    }

    on_vc_block_mutation(mutation_record) {
        if (mutation_record.target.classList.contains('w-combobox__menu')) {
            mutation_record.target.firstElementChild.classList.add('formbuilder-field-choices-group')
        }

        const dom_tooltip = mutation_record.target.firstElementChild?.nextElementSibling
        if (dom_tooltip?.id?.startsWith('tippy-')) {
            this.on_add_condition(dom_tooltip)
        }
    }

    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(placeholder, prefix, initialState, initialError);

        const dom_block = block.container[0].parentNode.parentNode.parentNode
        const dom_label = block.container[0].querySelector('[data-contentpath="label"] input')

        dom_label.addEventListener('change', () => this.on_label_change(dom_block, dom_label))

        const observer = new MutationObserver((mutationList, _) => {
            mutationList.forEach((mutation_record) => this.on_vc_block_mutation(mutation_record))
        });
        const dom_vc_block = block.container[0].parentNode.parentNode.parentNode.querySelector('[data-contentpath="visibility_condition"]');
        observer.observe(dom_vc_block, { attributes: false, childList: true, subtree: true });

        return block;
    }
}
window.telepath.register('forms.blocks.FormFieldBlock', FormFieldBlockDefinition);


class BooleanExpressionBlockDefinition extends window.wagtailStreamField.blocks.StreamBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(placeholder, prefix, initialState, initialError);

        if (block.container[0].parentNode.getAttribute('data-contentpath') === 'visibility_condition') {
            return block
        }

        const dom_vc = block.container[0].parentNode.parentNode.parentNode
        const dom_button = dom_vc.querySelector('button.w-panel__toggle');
        const dom_heading = dom_vc.querySelector('h2.w-panel__heading');

        update_vc_heading(dom_vc)
        dom_button.addEventListener('click', () => update_vc_heading(dom_vc));
        dom_heading.addEventListener('click', () => update_vc_heading(dom_vc));

        return block;
    }
}
window.telepath.register('forms.blocks.BooleanExpressionBlock', BooleanExpressionBlockDefinition);


class ConditionBlockDefinition extends window.wagtailStreamField.blocks.StructBlockDefinition {
    update_vc_hidden_fields(dom_block) {
        const dom_field_id = dom_block.querySelector('[data-contentpath="field_id"] input')
        const dom_field_label = dom_block.querySelector('[data-contentpath="field_label"] input')
    
        dom_field_id.value = window.form_builder_selected_choice.contentpath
        dom_field_label.value = window.form_builder_selected_choice.label
    
        window.form_builder_selected_choice = undefined
    }

    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(placeholder, prefix, initialState, initialError);

        const dom_vc = block.container[0].parentNode.parentNode.parentNode
        const dom_heading = dom_vc.querySelector('h2.w-panel__heading');
        const dom_button = dom_vc.querySelector('button.w-panel__toggle');
        const dom_value = dom_vc.querySelector('[data-contentpath="value"] input')
        const dom_operator = dom_vc.querySelector('[data-contentpath="operator"] select')

        if (window.form_builder_selected_choice !== undefined) {
            this.update_vc_hidden_fields(block.container[0])
        }
        update_vc_heading(dom_vc)
        dom_button.addEventListener('click', () => update_vc_heading(dom_vc));
        dom_heading.addEventListener('click', () => update_vc_heading(dom_vc));
        dom_value.addEventListener('change', () => update_vc_heading(dom_vc));
        dom_operator.addEventListener('change', () => update_vc_heading(dom_vc));

        console.log('fields:', get_fields())
        return block;
    }
}
window.telepath.register('forms.blocks.ConditionBlock', ConditionBlockDefinition);
