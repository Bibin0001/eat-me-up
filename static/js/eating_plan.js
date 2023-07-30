            function calculateMacros() {

                var total_calories = 0
                var total_proteins = 0
                var total_fats = 0
                var total_carbs = 0

                var breakfast_id = $('#id_breakfast').val()
                var lunch_id = $('#id_lunch').val()
                var dinner_id = $('#id_dinner').val()

                var breakfast_macros = [0, 0, 0, 0]
                var lunch_macros = [0, 0, 0, 0]
                var dinner_macros = [0, 0, 0, 0]
                // Gets all recipe macros of the chosen recipe. 0: calories, 1: proteins, 2: fats, 3: carbs
                if (breakfast_id) {

                    breakfast_macros = [parseFloat(attributes[breakfast_id][0]), parseFloat(attributes[breakfast_id][1]), parseFloat(attributes[breakfast_id][2]), parseFloat(attributes[breakfast_id][3])]
                }

                if (lunch_id) {

                    lunch_macros = [parseFloat(attributes[lunch_id][0]), parseFloat(attributes[lunch_id][1]), parseFloat(attributes[lunch_id][2]), parseFloat(attributes[lunch_id][3])]
                }

                if (dinner_id) {

                    dinner_macros = [parseFloat(attributes[dinner_id][0]), parseFloat(attributes[dinner_id][1]), parseFloat(attributes[dinner_id][2]), parseFloat(attributes[dinner_id][3])]
                }

                total_calories = breakfast_macros[0] + lunch_macros[0] + dinner_macros[0]
                total_proteins = breakfast_macros[1] + lunch_macros[1] + dinner_macros[1]
                total_fats = breakfast_macros[2] + lunch_macros[2] + dinner_macros[2]
                total_carbs = breakfast_macros[3] + lunch_macros[3] + dinner_macros[3]


                $('#total-calories').text(total_calories);
                $('#total-proteins').text(total_proteins);
                $('#total-fats').text(total_fats);
                $('#total-carbs').text(total_carbs);
            }