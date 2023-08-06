function onChange(e) {
    if (e.target.attributes.dataChange) {
        calculate()
    }
}

function resetSelect(target) {
    var parent = $(target).parent().children()


    var ingredient = parent[1].children[1]
    var quantity = parent[2].children[1]
    var measurements = parent[3].children[1]
    var element = attributes[ingredient.value];


    $(ingredient).prop("selectedIndex", 0)
    $(quantity).val('')
    $(measurements).prop("selectedIndex", 0)

    $(target).parent().fadeOut()
    calculate()
}


function calculate() {
    var elements = $('.base_element')

    var total_calories = 0
    var total_proteins = 0
    var total_fats = 0
    var total_carbs = 0

    for (var i = 0; i < elements.length; i++) {
        var element = elements[i]
        var selects = $(element).find('select')

        var inputValue = parseInt($(element).find('input').val())
        if (isNaN(inputValue)) {
            inputValue = 0
        }
        var select2Value = parseInt($(selects[1]).val())
        if (isNaN(select2Value)) {
            select2Value = 0
        }

        var calories = 0
        var proteins = 0
        var carbs = 0
        var fats = 0

        var select1Id = parseFloat($(selects[0]).val())
        var attribut = attributes[select1Id];
        if (attribut) {
            calories = parseFloat(attribut.calories)
            proteins = parseFloat(attribut.proteins)
            carbs = parseFloat(attribut.carbs)
            fats = parseFloat(attribut.fats)
        }

        var localTotalCalories = calories * inputValue * select2Value
        total_calories += localTotalCalories

        var localTotalProteins = proteins * inputValue * select2Value
        total_proteins += localTotalProteins

        var localTotalCarbs = carbs * inputValue * select2Value
        total_carbs += localTotalCarbs

        var localTotalFats = fats * inputValue * select2Value
        total_fats += localTotalFats


    }
    $('#total-calories').text(total_calories);
    $('#total-proteins').text(total_proteins);
    $('#total-fats').text(total_fats);
    $('#total-carbs').text(total_carbs);
}
