import { createRouter, createWebHistory } from 'vue-router';
import MatchList from '@/components/MatchList.vue';
import MatchDashboard from '@/components/MatchDashboard.vue';
import SignIn from '@/components/SignIn.vue';
import CreateMatch from '@/components/CreateMatch.vue';

const routes = [
    { path: '/', component: SignIn },
    { path: '/create-match', component: CreateMatch },
    { path: '/matches', component: MatchList },
    { path: '/matches/:id', component: MatchDashboard, props: true }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
