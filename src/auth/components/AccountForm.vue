<script setup>
import { ref, defineProps, defineEmits } from 'vue'

// Emit form submition event and values
const emit = defineEmits(['submit_event'])

const props = defineProps(['is_sign_up', 'username', 'password', 'confirm'])
const is_sign_up = ref(props.is_sign_up === 'true')

// Ref to vuetify form
const myForm = ref();

const username = ref(props.username)
const password = ref(props.password)
const confirm = ref(props.confirm)

// Client-side validation using vuetify array of rule functions
const usernameRules = [
    value => !!value || 'Field is required', //required
    value => {
        if (value.length >= 25) return 'Maximum length is 25 characters'
        else if (value.length <= 4) return 'Minimum length is 4 characters'
        else {
            return true
        }
    }, //min_len
    value => {
        if (!RegExp('^([a-zA-Z0-9\-\_]*)$').test(value)) {
            return "Username must:\n- Only contain alphanumerical characters, '-', and '_'"
        }
        else {
            return true
        }
    } //alphanumerical

]
// Use let since the value depends on 'is_sign_up'
let passwordRules = {}
if (is_sign_up.value) {
    passwordRules = [
        value => !!value || 'Field is required', // required
        value => {
            if (RegExp('^(.{0,7}|.{64,}|[^0-9]*|[^A-Z]*|[^a-z]*|[a-zA-Z0-9]*)$').test(value)) {
                return 'Password must be:\n- Between 8 - 64 characters long\n- Have at least 1 capital letter, 1 number, and 1 special character'
            }
            else {
                return true
            }
        }, // password_regex
        value => {
            if (value !== confirm.value) {
                return 'Password doesn\'t match confirmation'
            }
            else {
                return true
            }
        } // confirm_password
    ]

}
else {
    passwordRules = [
        value => !!value || 'Field is required', // required
        value => {
            if (RegExp('^(.{0,7}|.{64,}|[^0-9]*|[^A-Z]*|[^a-z]*|[a-zA-Z0-9]*)$').test(value)) {
                return 'Password must be:\n- Between 8 - 64 characters long\n- Have at least 1 capital letter, 1 number, and 1 special character'
            }
            else {
                return true
            }
        }, // password_regex
    ]
}
const confirmRules = [
    value => !!value || 'Field is required', // required
    value => {
        if (RegExp('^(.{0,7}|.{64,}|[^0-9]*|[^A-Z]*|[^a-z]*|[a-zA-Z0-9]*)$').test(value)) {
            return 'Password must be:\n- Between 8 - 64 characters long\n- Have at least 1 capital letter, 1 number, and 1 special character'
        }
        else {
            return true
        }
    }, // password_regex
]

// Wait for button's submit event to resolve
function on_submit() {
    // console.log("waiting...")
    // myForm.value?.validate().then(({ valid: isValid }) => {
    //     if (isValid){
            emit('submit_event', username.value, password.value, confirm.value)
    //     }
    // })
}

const visible1 = ref(false)
const visible2 = ref(false)
</script>


<!-- TODO: Prefill fields if user failed server-side validation -->



<template>
    <v-form ref="myForm">
        <v-container fluid>
            <v-row>
                <v-col cols="12" sm="6">
                    <div class="text-subtitle-1 text-medium-emphasis">Username</div>

                    <v-text-field v-model="username" :rules="usernameRules" density="compact" placeholder="Username"
                        prepend-inner-icon="mdi-email-outline" variant="outlined" autocomplete="username"></v-text-field>

                    <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                        Password

                        <a class="text-caption text-decoration-none text-blue" href="#" rel="noopener noreferrer"
                            target="_blank">
                            Forgot login password?</a>
                    </div>

                    <v-text-field v-model="password" :rules="passwordRules"
                        :append-inner-icon="visible1 ? 'mdi-eye-off' : 'mdi-eye'" :type="visible1 ? 'text' : 'password'"
                        density="compact" placeholder="Enter your password" prepend-inner-icon="mdi-lock-outline"
                        variant="outlined" @click:append-inner="visible1 = !visible1" :autocomplete="is_sign_up ? 'new-password' : 'current-password'"></v-text-field>

                    <v-text-field v-if="is_sign_up" v-model="confirm" :rules="confirmRules"
                        :append-inner-icon="visible2 ? 'mdi-eye-off' : 'mdi-eye'" :type="visible2 ? 'text' : 'password'"
                        density="compact" placeholder="Confirm your password" prepend-inner-icon="mdi-lock-outline"
                        variant="outlined" @click:append-inner="visible2 = !visible2" autocomplete="new-password"></v-text-field>
                    <!-- Depends on is_sign_in -->
                    <v-btn v-if="is_sign_up" @click="on_submit" type="submit" class="mb-8" color="blue" size="large"
                        variant="tonal" block>
                        Sign Up
                    </v-btn>
                    <v-btn v-else @click="on_submit" type="submit" class="mb-8" color="blue" size="large"
                        variant="tonal" block>
                        Sign In
                    </v-btn>
                </v-col>
            </v-row>
        </v-container>
    </v-form>
</template>