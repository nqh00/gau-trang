<template>
  <VContainer
    class="fill-height"
    fluid>
    <VRow justify="center">
      <VCol
        sm="6"
        md="6"
        lg="5">
        <img src="./icon.png" alt="Gautrang Logo" class="text-center">
        <LoginForm
          :user="currentUser"
          @change="resetCurrentUser" />
        <p v-if="disclaimer" class="text-p mt-6 text-center">
          <JSafeHtml :html="disclaimer" />
        </p>
      </VCol>
    </VRow>
  </VContainer>
</template>

<route lang="yaml">
meta:
  layout:
    name: server
</route>

<script setup lang="ts">
import type { UserDto } from '@jellyfin/sdk/lib/generated-client';
import { ref, shallowRef, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute, useRouter } from 'vue-router';
import { watchImmediate } from '@vueuse/core';
import { remote } from '@/plugins/remote';
import { getJSONConfig } from '@/utils/external-config';
import { isConnectedToServer } from '@/store';

const jsonConfig = await getJSONConfig();
const { t } = useI18n();
const route = useRoute();
const router = useRouter();

route.meta.title = t('login');

watchImmediate(isConnectedToServer, async () => {
  if (!isConnectedToServer.value) {
    await router.replace('/server/login');
  }
});

const disclaimer = computed(() => remote.auth.currentServer?.BrandingOptions.LoginDisclaimer);
const publicUsers = computed(() => remote.auth.currentServer?.PublicUsers ?? []);

const loginAsOther = shallowRef(false);
const currentUser = ref<UserDto>();

/**
 * Sets the current user for public user login
 */
async function setCurrentUser(user: UserDto): Promise<void> {
  if (!user.HasPassword && user.Name) {
    // If the user doesn't have a password, avoid showing the password form
    await remote.auth.loginUser(user.Name, '');
    await router.replace('/');
  } else {
    currentUser.value = user;
  }
}

/**
 * Resets the currently selected user
 */
function resetCurrentUser(): void {
  currentUser.value = undefined;
  loginAsOther.value = false;
}
</script>
