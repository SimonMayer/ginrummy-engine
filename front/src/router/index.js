import { createRouter, createWebHistory } from 'vue-router';
import MatchList from '../components/MatchList.vue';
import MatchDetails from '../components/MatchDetails.vue';
import SignIn from '../components/SignIn.vue';

const routes = [
    { path: '/', component: SignIn },
    { path: '/matches', component: MatchList },
    { path: '/matches/:id', component: MatchDetails, props: true }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
