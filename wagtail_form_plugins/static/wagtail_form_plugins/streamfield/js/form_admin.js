// https://jasonwatmore.com/vanilla-js-slugify-a-string-in-javascript
function slugify(input) {
    return !input ? '' : input.toLowerCase().trim().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
        .replace(/[^a-z0-9\s-]/g, ' ').trim().replace(/[\s-]+/g, '_');
}

function on_field_label_changed(dom_field_block) {
    console.log('=== field label changed');
    const dom_field_label_input = dom_field_block.querySelector('[data-contentpath=label] input')
    const dom_field_id_input = dom_field_block.querySelector('[data-contentpath=identifier] input')
    if (dom_field_id_input.value === "") {
        dom_field_id_input.value = slugify(dom_field_label_input.value);
    }
}

class FormFieldBlockDefinition extends window.wagtailStreamField.blocks.StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(placeholder, prefix, initialState, initialError);
        const dom_field_block = block.container[0];
        const dom_field_label = dom_field_block.querySelector('[data-contentpath=label]');
        dom_field_label.addEventListener('change', () => on_field_label_changed(dom_field_block))
        return block;
    }
}
window.telepath.register('forms.blocks.FormFieldBlock', FormFieldBlockDefinition);
