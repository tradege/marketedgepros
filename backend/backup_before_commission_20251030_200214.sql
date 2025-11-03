--
-- PostgreSQL database dump
--

\restrict c6PrtGfLBRZmnbnN1sVrUogEsPc9chGWr2Uf6Lw9eykac1vYbcZpciArV3AgOqf

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6 (Ubuntu 17.6-0ubuntu0.25.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: update_blog_posts_updated_at(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_blog_posts_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


--
-- Name: update_faqs_updated_at(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_faqs_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


--
-- Name: update_payment_approval_requests_updated_at(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_payment_approval_requests_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


--
-- Name: update_support_tickets_updated_at(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_support_tickets_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: affiliate_commissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.affiliate_commissions (
    id integer NOT NULL,
    affiliate_user_id integer NOT NULL,
    referral_id integer,
    amount numeric(10,2) NOT NULL,
    type character varying(20) DEFAULT 'one_time'::character varying,
    status character varying(20) DEFAULT 'pending'::character varying,
    description character varying(500),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    approved_at timestamp without time zone,
    paid_at timestamp without time zone,
    payout_id integer
);


--
-- Name: affiliate_commissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.affiliate_commissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: affiliate_commissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.affiliate_commissions_id_seq OWNED BY public.affiliate_commissions.id;


--
-- Name: affiliate_links; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.affiliate_links (
    id integer NOT NULL,
    user_id integer NOT NULL,
    code character varying(50) NOT NULL,
    name character varying(100),
    clicks integer DEFAULT 0,
    conversions integer DEFAULT 0,
    total_revenue numeric(10,2) DEFAULT 0,
    total_commission numeric(10,2) DEFAULT 0,
    commission_rate numeric(5,2) DEFAULT 10.00,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    last_click_at timestamp without time zone
);


--
-- Name: affiliate_links_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.affiliate_links_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: affiliate_links_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.affiliate_links_id_seq OWNED BY public.affiliate_links.id;


--
-- Name: affiliate_payouts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.affiliate_payouts (
    id integer NOT NULL,
    affiliate_user_id integer NOT NULL,
    amount numeric(10,2) NOT NULL,
    method character varying(50),
    payment_details jsonb,
    status character varying(20) DEFAULT 'pending'::character varying,
    notes text,
    transaction_id character varying(100),
    requested_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    processed_at timestamp without time zone,
    completed_at timestamp without time zone
);


--
-- Name: affiliate_payouts_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.affiliate_payouts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: affiliate_payouts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.affiliate_payouts_id_seq OWNED BY public.affiliate_payouts.id;


--
-- Name: affiliate_referrals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.affiliate_referrals (
    id integer NOT NULL,
    affiliate_link_id integer NOT NULL,
    affiliate_user_id integer NOT NULL,
    referred_user_id integer,
    ip_address character varying(45),
    user_agent character varying(500),
    landing_page character varying(500),
    status character varying(20) DEFAULT 'pending'::character varying,
    program_id integer,
    purchase_amount numeric(10,2),
    commission_amount numeric(10,2),
    click_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    conversion_date timestamp without time zone
);


--
-- Name: affiliate_referrals_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.affiliate_referrals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: affiliate_referrals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.affiliate_referrals_id_seq OWNED BY public.affiliate_referrals.id;


--
-- Name: affiliate_settings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.affiliate_settings (
    id integer NOT NULL,
    default_commission_rate numeric(5,2) DEFAULT 10.00,
    min_payout_amount numeric(10,2) DEFAULT 50.00,
    cookie_duration_days integer DEFAULT 30,
    is_active boolean DEFAULT true,
    auto_approve_affiliates boolean DEFAULT false,
    auto_approve_commissions boolean DEFAULT false,
    terms_and_conditions text,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: affiliate_settings_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.affiliate_settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: affiliate_settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.affiliate_settings_id_seq OWNED BY public.affiliate_settings.id;


--
-- Name: agents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.agents (
    id integer NOT NULL,
    agent_code character varying(50) NOT NULL,
    user_id integer NOT NULL,
    commission_rate numeric(5,2) NOT NULL,
    total_earned numeric(12,2) NOT NULL,
    total_withdrawn numeric(12,2) NOT NULL,
    pending_balance numeric(12,2) NOT NULL,
    referral_count integer NOT NULL,
    active_referrals integer NOT NULL,
    total_sales numeric(12,2) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: agents_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.agents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: agents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.agents_id_seq OWNED BY public.agents.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: blog_posts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.blog_posts (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    slug character varying(250) NOT NULL,
    excerpt text,
    content text NOT NULL,
    featured_image character varying(500),
    featured_image_alt character varying(200),
    category character varying(50) NOT NULL,
    tags character varying(500),
    meta_title character varying(200),
    meta_description character varying(300),
    meta_keywords character varying(500),
    author_id integer NOT NULL,
    status character varying(20) DEFAULT 'draft'::character varying NOT NULL,
    published_at timestamp without time zone,
    view_count integer DEFAULT 0,
    featured boolean DEFAULT false,
    reading_time integer DEFAULT 5,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: TABLE blog_posts; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.blog_posts IS 'Blog posts for content management system';


--
-- Name: COLUMN blog_posts.slug; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.blog_posts.slug IS 'URL-friendly unique identifier for the post';


--
-- Name: COLUMN blog_posts.status; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.blog_posts.status IS 'Post status: draft, published, or archived';


--
-- Name: COLUMN blog_posts.featured; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.blog_posts.featured IS 'Whether the post should be featured on the homepage';


--
-- Name: COLUMN blog_posts.reading_time; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.blog_posts.reading_time IS 'Estimated reading time in minutes';


--
-- Name: blog_posts_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.blog_posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: blog_posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.blog_posts_id_seq OWNED BY public.blog_posts.id;


--
-- Name: challenges; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.challenges (
    id integer NOT NULL,
    user_id integer NOT NULL,
    program_id integer NOT NULL,
    status character varying(20) NOT NULL,
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    passed_at timestamp without time zone,
    account_number character varying(50),
    initial_balance numeric(12,2),
    current_balance numeric(12,2),
    total_profit numeric(12,2),
    total_loss numeric(12,2),
    max_drawdown numeric(12,2),
    current_phase integer,
    total_phases integer,
    payment_status character varying(20),
    payment_id character varying(100),
    addons jsonb,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    created_by integer,
    payment_type character varying(20) DEFAULT 'credit_card'::character varying NOT NULL,
    approval_status character varying(20) DEFAULT 'approved'::character varying NOT NULL,
    approved_by integer,
    approved_at timestamp without time zone,
    rejection_reason text,
    CONSTRAINT valid_approval_status_challenges CHECK (((approval_status)::text = ANY ((ARRAY['pending'::character varying, 'approved'::character varying, 'rejected'::character varying])::text[]))),
    CONSTRAINT valid_payment_type_challenges CHECK (((payment_type)::text = ANY ((ARRAY['credit_card'::character varying, 'cash'::character varying, 'free'::character varying])::text[])))
);


--
-- Name: COLUMN challenges.payment_type; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.challenges.payment_type IS 'credit_card, cash, free';


--
-- Name: COLUMN challenges.approval_status; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.challenges.approval_status IS 'pending, approved, rejected (only for cash/free payments)';


--
-- Name: challenges_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.challenges_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: challenges_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.challenges_id_seq OWNED BY public.challenges.id;


--
-- Name: commission_balances; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.commission_balances (
    id integer NOT NULL,
    user_id integer NOT NULL,
    total_earned numeric(10,2) DEFAULT 0.00 NOT NULL,
    available_balance numeric(10,2) DEFAULT 0.00 NOT NULL,
    pending_balance numeric(10,2) DEFAULT 0.00 NOT NULL,
    withdrawn_total numeric(10,2) DEFAULT 0.00 NOT NULL,
    total_commissions integer DEFAULT 0 NOT NULL,
    last_commission_at timestamp without time zone,
    last_withdrawal_at timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: TABLE commission_balances; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.commission_balances IS 'Cached commission balances for performance';


--
-- Name: commission_balances_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.commission_balances_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: commission_balances_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.commission_balances_id_seq OWNED BY public.commission_balances.id;


--
-- Name: commission_rules; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.commission_rules (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    rule_type character varying(50) NOT NULL,
    target_role character varying(20) NOT NULL,
    level_1_rate numeric(5,2) DEFAULT 0.00,
    level_2_rate numeric(5,2) DEFAULT 0.00,
    level_3_rate numeric(5,2) DEFAULT 0.00,
    level_4_rate numeric(5,2) DEFAULT 0.00,
    level_5_rate numeric(5,2) DEFAULT 0.00,
    max_levels integer DEFAULT 5,
    is_active boolean DEFAULT true NOT NULL,
    min_amount numeric(10,2) DEFAULT 0.00,
    max_amount numeric(10,2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: TABLE commission_rules; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.commission_rules IS 'Commission calculation rules for MLM system';


--
-- Name: commission_rules_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.commission_rules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: commission_rules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.commission_rules_id_seq OWNED BY public.commission_rules.id;


--
-- Name: commission_withdrawals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.commission_withdrawals (
    id integer NOT NULL,
    user_id integer NOT NULL,
    amount numeric(10,2) NOT NULL,
    currency character varying(3) DEFAULT 'USD'::character varying,
    payment_method character varying(50) NOT NULL,
    payment_details jsonb,
    status character varying(20) DEFAULT 'pending'::character varying NOT NULL,
    requested_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    approved_at timestamp without time zone,
    approved_by integer,
    completed_at timestamp without time zone,
    rejected_at timestamp without time zone,
    rejection_reason text,
    transaction_reference character varying(100),
    notes text,
    admin_notes text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: TABLE commission_withdrawals; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.commission_withdrawals IS 'Commission withdrawal requests';


--
-- Name: commission_withdrawals_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.commission_withdrawals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: commission_withdrawals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.commission_withdrawals_id_seq OWNED BY public.commission_withdrawals.id;


--
-- Name: commissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.commissions (
    id integer NOT NULL,
    agent_id integer NOT NULL,
    referral_id integer NOT NULL,
    challenge_id integer NOT NULL,
    sale_amount numeric(12,2) NOT NULL,
    commission_rate numeric(5,2) NOT NULL,
    commission_amount numeric(12,2) NOT NULL,
    status character varying(20) NOT NULL,
    approved_at timestamp without time zone,
    paid_at timestamp without time zone,
    payment_method character varying(50),
    transaction_id character varying(100),
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    user_id integer,
    source_type character varying(50) DEFAULT 'challenge'::character varying,
    source_id integer,
    source_user_id integer,
    rule_id integer,
    level integer DEFAULT 1,
    base_amount numeric(10,2),
    approved_by integer,
    payment_reference character varying(100),
    notes text,
    admin_notes text
);


--
-- Name: commissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.commissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: commissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.commissions_id_seq OWNED BY public.commissions.id;


--
-- Name: course_enrollments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.course_enrollments (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    name character varying(255),
    enrolled_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    module_1_sent boolean DEFAULT false,
    module_1_sent_at timestamp without time zone,
    module_2_sent boolean DEFAULT false,
    module_2_sent_at timestamp without time zone,
    module_3_sent boolean DEFAULT false,
    module_3_sent_at timestamp without time zone,
    module_4_sent boolean DEFAULT false,
    module_4_sent_at timestamp without time zone,
    module_5_sent boolean DEFAULT false,
    module_5_sent_at timestamp without time zone,
    last_email_opened_at timestamp without time zone,
    unsubscribed boolean DEFAULT false,
    unsubscribed_at timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: course_enrollments_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.course_enrollments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: course_enrollments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.course_enrollments_id_seq OWNED BY public.course_enrollments.id;


--
-- Name: email_queue; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.email_queue (
    id integer NOT NULL,
    user_id integer NOT NULL,
    to_email character varying(255) NOT NULL,
    subject character varying(255) NOT NULL,
    body text NOT NULL,
    html_body text,
    status character varying(20),
    attempts integer,
    max_attempts integer,
    error_message text,
    sent_at timestamp without time zone,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: email_queue_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.email_queue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: email_queue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.email_queue_id_seq OWNED BY public.email_queue.id;


--
-- Name: email_verification_tokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.email_verification_tokens (
    id integer NOT NULL,
    user_id integer NOT NULL,
    code character varying(6) NOT NULL,
    token character varying(64) NOT NULL,
    expires_at timestamp without time zone NOT NULL,
    used boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: email_verification_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.email_verification_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: email_verification_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.email_verification_tokens_id_seq OWNED BY public.email_verification_tokens.id;


--
-- Name: faqs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.faqs (
    id integer NOT NULL,
    question character varying(500) NOT NULL,
    answer text NOT NULL,
    category character varying(50) NOT NULL,
    "order" integer DEFAULT 0,
    is_featured boolean DEFAULT false,
    is_published boolean DEFAULT true,
    view_count integer DEFAULT 0,
    helpful_count integer DEFAULT 0,
    not_helpful_count integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: faqs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.faqs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: faqs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.faqs_id_seq OWNED BY public.faqs.id;


--
-- Name: lead_activities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lead_activities (
    id integer NOT NULL,
    lead_id integer NOT NULL,
    user_id integer NOT NULL,
    activity_type character varying(50) NOT NULL,
    subject character varying(200),
    description text,
    outcome character varying(50),
    scheduled_at timestamp without time zone,
    completed boolean,
    completed_at timestamp without time zone,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: lead_activities_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.lead_activities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: lead_activities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.lead_activities_id_seq OWNED BY public.lead_activities.id;


--
-- Name: lead_notes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lead_notes (
    id integer NOT NULL,
    lead_id integer NOT NULL,
    user_id integer NOT NULL,
    content text NOT NULL,
    is_important boolean,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: lead_notes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.lead_notes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: lead_notes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.lead_notes_id_seq OWNED BY public.lead_notes.id;


--
-- Name: leads; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.leads (
    id integer NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    phone character varying(20),
    country_code character varying(2),
    status character varying(20) NOT NULL,
    source character varying(50),
    score integer,
    assigned_to integer,
    assigned_at timestamp without time zone,
    interested_program_id integer,
    budget numeric(10,2),
    converted_to_user_id integer,
    converted_at timestamp without time zone,
    lost_reason character varying(50),
    lost_notes text,
    lost_at timestamp without time zone,
    company character varying(200),
    job_title character varying(100),
    notes text,
    tags character varying(500),
    last_contacted_at timestamp without time zone,
    next_follow_up timestamp without time zone,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: leads_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.leads_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: leads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.leads_id_seq OWNED BY public.leads.id;


--
-- Name: notification_preferences; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notification_preferences (
    id integer NOT NULL,
    user_id integer NOT NULL,
    in_app_withdrawal boolean,
    in_app_commission boolean,
    in_app_kyc boolean,
    in_app_system boolean,
    in_app_payment boolean,
    in_app_challenge boolean,
    email_withdrawal boolean,
    email_commission boolean,
    email_kyc boolean,
    email_system boolean,
    email_payment boolean,
    email_challenge boolean,
    email_enabled boolean,
    email_frequency character varying(20),
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: notification_preferences_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.notification_preferences_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: notification_preferences_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.notification_preferences_id_seq OWNED BY public.notification_preferences.id;


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notifications (
    id integer NOT NULL,
    user_id integer NOT NULL,
    type character varying(50) NOT NULL,
    title character varying(255) NOT NULL,
    message text NOT NULL,
    data json,
    priority character varying(20),
    is_read boolean,
    read_at timestamp without time zone,
    is_deleted boolean,
    deleted_at timestamp without time zone,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;


--
-- Name: password_reset_tokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.password_reset_tokens (
    id integer NOT NULL,
    user_id integer NOT NULL,
    code character varying(6) NOT NULL,
    token character varying(64) NOT NULL,
    expires_at timestamp without time zone NOT NULL,
    used boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.password_reset_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.password_reset_tokens_id_seq OWNED BY public.password_reset_tokens.id;


--
-- Name: payment_approval_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.payment_approval_requests (
    id integer NOT NULL,
    challenge_id integer,
    payment_id integer,
    requested_by integer NOT NULL,
    requested_for integer NOT NULL,
    amount numeric(10,2) NOT NULL,
    payment_type character varying(20) NOT NULL,
    status character varying(20) DEFAULT 'pending'::character varying NOT NULL,
    reviewed_by integer,
    reviewed_at timestamp without time zone,
    rejection_reason text,
    admin_notes text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_payment_type CHECK (((payment_type)::text = ANY ((ARRAY['cash'::character varying, 'free'::character varying])::text[]))),
    CONSTRAINT valid_status CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'approved'::character varying, 'rejected'::character varying])::text[])))
);


--
-- Name: payment_approval_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.payment_approval_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: payment_approval_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.payment_approval_requests_id_seq OWNED BY public.payment_approval_requests.id;


--
-- Name: payments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.payments (
    id integer NOT NULL,
    user_id integer NOT NULL,
    amount numeric(10,2) NOT NULL,
    currency character varying(3),
    payment_method character varying(50),
    transaction_id character varying(255),
    status character varying(50),
    purpose character varying(100),
    reference_id integer,
    provider_response text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    completed_at timestamp without time zone,
    payment_type character varying(20) DEFAULT 'credit_card'::character varying NOT NULL,
    approval_status character varying(20) DEFAULT 'approved'::character varying NOT NULL,
    approved_by integer,
    approved_at timestamp without time zone,
    rejection_reason text,
    admin_notes text,
    CONSTRAINT valid_approval_status CHECK (((approval_status)::text = ANY ((ARRAY['pending'::character varying, 'approved'::character varying, 'rejected'::character varying])::text[]))),
    CONSTRAINT valid_payment_type CHECK (((payment_type)::text = ANY ((ARRAY['credit_card'::character varying, 'cash'::character varying, 'free'::character varying])::text[])))
);


--
-- Name: COLUMN payments.payment_type; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.payments.payment_type IS 'credit_card, cash, free';


--
-- Name: COLUMN payments.approval_status; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.payments.approval_status IS 'pending, approved, rejected (only for cash/free payments)';


--
-- Name: payments_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.payments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.payments_id_seq OWNED BY public.payments.id;


--
-- Name: program_addons; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.program_addons (
    id integer NOT NULL,
    program_id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    price numeric(10,2) NOT NULL,
    price_type character varying(20),
    benefits jsonb,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: program_addons_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.program_addons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: program_addons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.program_addons_id_seq OWNED BY public.program_addons.id;


--
-- Name: referrals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.referrals (
    id integer NOT NULL,
    agent_id integer NOT NULL,
    referred_user_id integer NOT NULL,
    referral_code character varying(50) NOT NULL,
    ip_address character varying(45),
    user_agent character varying(500),
    status character varying(20) NOT NULL,
    first_purchase_at timestamp without time zone,
    total_purchases integer NOT NULL,
    total_spent numeric(12,2) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: referrals_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.referrals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: referrals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.referrals_id_seq OWNED BY public.referrals.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    label character varying(100) NOT NULL,
    label_he character varying(100),
    color character varying(100),
    icon character varying(10),
    hierarchy integer NOT NULL,
    permissions json,
    is_active boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: support_articles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.support_articles (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    content text NOT NULL,
    excerpt character varying(500),
    category character varying(100) NOT NULL,
    subcategory character varying(100),
    tags jsonb,
    meta_description character varying(160),
    meta_keywords character varying(255),
    status character varying(20) DEFAULT 'draft'::character varying NOT NULL,
    published_at timestamp without time zone,
    author_id integer,
    views integer DEFAULT 0,
    helpful_count integer DEFAULT 0,
    not_helpful_count integer DEFAULT 0,
    "order" integer DEFAULT 0,
    featured boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_status CHECK (((status)::text = ANY ((ARRAY['draft'::character varying, 'published'::character varying, 'archived'::character varying])::text[])))
);


--
-- Name: support_articles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.support_articles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: support_articles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.support_articles_id_seq OWNED BY public.support_articles.id;


--
-- Name: support_tickets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.support_tickets (
    id integer NOT NULL,
    ticket_number character varying(20) NOT NULL,
    user_id integer,
    email character varying(255) NOT NULL,
    name character varying(200) NOT NULL,
    subject character varying(500) NOT NULL,
    description text NOT NULL,
    category character varying(50) NOT NULL,
    priority character varying(20) DEFAULT 'medium'::character varying,
    status character varying(20) DEFAULT 'open'::character varying,
    assigned_to integer,
    attachments text,
    first_response_at timestamp without time zone,
    resolved_at timestamp without time zone,
    closed_at timestamp without time zone,
    rating integer,
    feedback text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT support_tickets_rating_check CHECK (((rating >= 1) AND (rating <= 5)))
);


--
-- Name: support_tickets_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.support_tickets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: support_tickets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.support_tickets_id_seq OWNED BY public.support_tickets.id;


--
-- Name: tenants; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tenants (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    subdomain character varying(100) NOT NULL,
    custom_domain character varying(255),
    status character varying(20) NOT NULL,
    tier character varying(20) NOT NULL,
    parent_id integer,
    logo_url character varying(500),
    favicon_url character varying(500),
    primary_color character varying(7),
    secondary_color character varying(7),
    accent_color character varying(7),
    custom_css text,
    settings jsonb,
    contact_email character varying(255),
    contact_phone character varying(20),
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: tenants_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tenants_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tenants_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tenants_id_seq OWNED BY public.tenants.id;


--
-- Name: ticket_messages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ticket_messages (
    id integer NOT NULL,
    ticket_id integer NOT NULL,
    user_id integer,
    email character varying(255),
    name character varying(200),
    message text NOT NULL,
    is_staff boolean DEFAULT false,
    is_internal boolean DEFAULT false,
    attachments text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: ticket_messages_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ticket_messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ticket_messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ticket_messages_id_seq OWNED BY public.ticket_messages.id;


--
-- Name: trades; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trades (
    id integer NOT NULL,
    challenge_id integer NOT NULL,
    ticket character varying(100),
    symbol character varying(20) NOT NULL,
    trade_type character varying(10) NOT NULL,
    volume numeric(15,2) NOT NULL,
    open_price numeric(15,5) NOT NULL,
    close_price numeric(15,5),
    stop_loss numeric(15,5),
    take_profit numeric(15,5),
    profit numeric(15,2),
    commission numeric(10,2),
    swap numeric(10,2),
    status character varying(20),
    open_time timestamp without time zone NOT NULL,
    close_time timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


--
-- Name: trades_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.trades_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: trades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.trades_id_seq OWNED BY public.trades.id;


--
-- Name: trading_programs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trading_programs (
    id integer NOT NULL,
    tenant_id integer NOT NULL,
    name character varying(255) NOT NULL,
    type character varying(50) NOT NULL,
    description text,
    account_size numeric(12,2) NOT NULL,
    profit_target numeric(5,2),
    max_daily_loss numeric(5,2),
    max_total_loss numeric(5,2),
    price numeric(10,2) NOT NULL,
    profit_split numeric(5,2),
    rules jsonb,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: trading_programs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.trading_programs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: trading_programs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.trading_programs_id_seq OWNED BY public.trading_programs.id;


--
-- Name: transactions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.transactions (
    id integer NOT NULL,
    wallet_id integer NOT NULL,
    type character varying(50) NOT NULL,
    amount numeric(12,2) NOT NULL,
    balance_type character varying(20) NOT NULL,
    balance_before numeric(12,2) NOT NULL,
    balance_after numeric(12,2) NOT NULL,
    reference_type character varying(50),
    reference_id integer,
    description character varying(255),
    notes text,
    created_by integer,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: transactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.transactions_id_seq OWNED BY public.transactions.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    phone character varying(20),
    country_code character varying(2),
    date_of_birth date,
    avatar_url character varying(500),
    is_active boolean NOT NULL,
    is_verified boolean NOT NULL,
    email_verified_at timestamp without time zone,
    two_factor_enabled boolean NOT NULL,
    two_factor_secret character varying(32),
    kyc_status character varying(20),
    kyc_submitted_at timestamp without time zone,
    kyc_verified_at timestamp without time zone,
    kyc_approved_at timestamp without time zone,
    kyc_approved_by integer,
    kyc_rejected_at timestamp without time zone,
    kyc_rejected_by integer,
    kyc_rejection_reason text,
    kyc_admin_notes text,
    kyc_id_status character varying(20),
    kyc_id_url character varying(500),
    kyc_id_uploaded_at timestamp without time zone,
    kyc_id_notes text,
    kyc_address_status character varying(20),
    kyc_address_url character varying(500),
    kyc_address_uploaded_at timestamp without time zone,
    kyc_address_notes text,
    kyc_selfie_status character varying(20),
    kyc_selfie_url character varying(500),
    kyc_selfie_uploaded_at timestamp without time zone,
    kyc_selfie_notes text,
    kyc_bank_status character varying(20),
    kyc_bank_url character varying(500),
    kyc_bank_uploaded_at timestamp without time zone,
    kyc_bank_notes text,
    role character varying(20) NOT NULL,
    parent_id integer,
    level integer NOT NULL,
    tree_path character varying(500),
    commission_rate numeric(5,2),
    tenant_id integer,
    last_login_at timestamp without time zone,
    last_login_ip character varying(45),
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    referral_code character varying(20),
    referred_by_code character varying(20),
    referred_by_user_id integer,
    has_purchased_program boolean DEFAULT false,
    first_purchase_at timestamp without time zone,
    total_purchases integer DEFAULT 0,
    total_referrals integer DEFAULT 0,
    active_referrals integer DEFAULT 0,
    referral_earnings numeric(10,2) DEFAULT 0.00,
    can_create_same_role boolean DEFAULT false NOT NULL
);


--
-- Name: COLUMN users.referral_code; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.referral_code IS 'Unique referral code for this user (agents/masters/supermasters)';


--
-- Name: COLUMN users.referred_by_code; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.referred_by_code IS 'Referral code used when signing up';


--
-- Name: COLUMN users.referred_by_user_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.referred_by_user_id IS 'User ID who referred this user';


--
-- Name: COLUMN users.has_purchased_program; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.has_purchased_program IS 'Whether user has purchased any program';


--
-- Name: COLUMN users.first_purchase_at; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.first_purchase_at IS 'Timestamp of first program purchase';


--
-- Name: COLUMN users.total_purchases; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.total_purchases IS 'Total number of programs purchased';


--
-- Name: COLUMN users.total_referrals; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.total_referrals IS 'Total number of users referred';


--
-- Name: COLUMN users.active_referrals; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.active_referrals IS 'Number of active referred users';


--
-- Name: COLUMN users.referral_earnings; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.referral_earnings IS 'Total earnings from referrals';


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: verification_attempts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.verification_attempts (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    code_entered character varying(6) NOT NULL,
    success boolean NOT NULL,
    ip_address character varying(45),
    user_agent character varying(500),
    failure_reason character varying(200),
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: verification_attempts_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.verification_attempts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: verification_attempts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.verification_attempts_id_seq OWNED BY public.verification_attempts.id;


--
-- Name: wallets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.wallets (
    id integer NOT NULL,
    user_id integer NOT NULL,
    main_balance numeric(12,2) NOT NULL,
    commission_balance numeric(12,2) NOT NULL,
    bonus_balance numeric(12,2) NOT NULL,
    last_transaction_at timestamp without time zone,
    is_active boolean NOT NULL,
    notes text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: wallets_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.wallets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: wallets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.wallets_id_seq OWNED BY public.wallets.id;


--
-- Name: withdrawals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.withdrawals (
    id integer NOT NULL,
    agent_id integer NOT NULL,
    amount numeric(12,2) NOT NULL,
    fee numeric(12,2) NOT NULL,
    net_amount numeric(12,2) NOT NULL,
    payment_method character varying(50) NOT NULL,
    payment_details json,
    status character varying(20) NOT NULL,
    approved_by integer,
    approved_at timestamp without time zone,
    processed_at timestamp without time zone,
    completed_at timestamp without time zone,
    transaction_id character varying(100),
    rejection_reason text,
    notes text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: withdrawals_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.withdrawals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: withdrawals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.withdrawals_id_seq OWNED BY public.withdrawals.id;


--
-- Name: affiliate_commissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_commissions ALTER COLUMN id SET DEFAULT nextval('public.affiliate_commissions_id_seq'::regclass);


--
-- Name: affiliate_links id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_links ALTER COLUMN id SET DEFAULT nextval('public.affiliate_links_id_seq'::regclass);


--
-- Name: affiliate_payouts id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_payouts ALTER COLUMN id SET DEFAULT nextval('public.affiliate_payouts_id_seq'::regclass);


--
-- Name: affiliate_referrals id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_referrals ALTER COLUMN id SET DEFAULT nextval('public.affiliate_referrals_id_seq'::regclass);


--
-- Name: affiliate_settings id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_settings ALTER COLUMN id SET DEFAULT nextval('public.affiliate_settings_id_seq'::regclass);


--
-- Name: agents id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agents ALTER COLUMN id SET DEFAULT nextval('public.agents_id_seq'::regclass);


--
-- Name: blog_posts id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_posts ALTER COLUMN id SET DEFAULT nextval('public.blog_posts_id_seq'::regclass);


--
-- Name: challenges id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.challenges ALTER COLUMN id SET DEFAULT nextval('public.challenges_id_seq'::regclass);


--
-- Name: commission_balances id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_balances ALTER COLUMN id SET DEFAULT nextval('public.commission_balances_id_seq'::regclass);


--
-- Name: commission_rules id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_rules ALTER COLUMN id SET DEFAULT nextval('public.commission_rules_id_seq'::regclass);


--
-- Name: commission_withdrawals id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_withdrawals ALTER COLUMN id SET DEFAULT nextval('public.commission_withdrawals_id_seq'::regclass);


--
-- Name: commissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commissions ALTER COLUMN id SET DEFAULT nextval('public.commissions_id_seq'::regclass);


--
-- Name: course_enrollments id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course_enrollments ALTER COLUMN id SET DEFAULT nextval('public.course_enrollments_id_seq'::regclass);


--
-- Name: email_queue id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_queue ALTER COLUMN id SET DEFAULT nextval('public.email_queue_id_seq'::regclass);


--
-- Name: email_verification_tokens id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_verification_tokens ALTER COLUMN id SET DEFAULT nextval('public.email_verification_tokens_id_seq'::regclass);


--
-- Name: faqs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.faqs ALTER COLUMN id SET DEFAULT nextval('public.faqs_id_seq'::regclass);


--
-- Name: lead_activities id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lead_activities ALTER COLUMN id SET DEFAULT nextval('public.lead_activities_id_seq'::regclass);


--
-- Name: lead_notes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lead_notes ALTER COLUMN id SET DEFAULT nextval('public.lead_notes_id_seq'::regclass);


--
-- Name: leads id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.leads ALTER COLUMN id SET DEFAULT nextval('public.leads_id_seq'::regclass);


--
-- Name: notification_preferences id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_preferences ALTER COLUMN id SET DEFAULT nextval('public.notification_preferences_id_seq'::regclass);


--
-- Name: notifications id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);


--
-- Name: password_reset_tokens id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_reset_tokens ALTER COLUMN id SET DEFAULT nextval('public.password_reset_tokens_id_seq'::regclass);


--
-- Name: payment_approval_requests id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment_approval_requests ALTER COLUMN id SET DEFAULT nextval('public.payment_approval_requests_id_seq'::regclass);


--
-- Name: payments id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payments ALTER COLUMN id SET DEFAULT nextval('public.payments_id_seq'::regclass);


--
-- Name: program_addons id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.program_addons ALTER COLUMN id SET DEFAULT nextval('public.program_addons_id_seq'::regclass);


--
-- Name: referrals id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.referrals ALTER COLUMN id SET DEFAULT nextval('public.referrals_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: support_articles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_articles ALTER COLUMN id SET DEFAULT nextval('public.support_articles_id_seq'::regclass);


--
-- Name: support_tickets id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_tickets ALTER COLUMN id SET DEFAULT nextval('public.support_tickets_id_seq'::regclass);


--
-- Name: tenants id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tenants ALTER COLUMN id SET DEFAULT nextval('public.tenants_id_seq'::regclass);


--
-- Name: ticket_messages id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ticket_messages ALTER COLUMN id SET DEFAULT nextval('public.ticket_messages_id_seq'::regclass);


--
-- Name: trades id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trades ALTER COLUMN id SET DEFAULT nextval('public.trades_id_seq'::regclass);


--
-- Name: trading_programs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trading_programs ALTER COLUMN id SET DEFAULT nextval('public.trading_programs_id_seq'::regclass);


--
-- Name: transactions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transactions ALTER COLUMN id SET DEFAULT nextval('public.transactions_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: verification_attempts id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.verification_attempts ALTER COLUMN id SET DEFAULT nextval('public.verification_attempts_id_seq'::regclass);


--
-- Name: wallets id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wallets ALTER COLUMN id SET DEFAULT nextval('public.wallets_id_seq'::regclass);


--
-- Name: withdrawals id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.withdrawals ALTER COLUMN id SET DEFAULT nextval('public.withdrawals_id_seq'::regclass);


--
-- Data for Name: affiliate_commissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.affiliate_commissions (id, affiliate_user_id, referral_id, amount, type, status, description, created_at, approved_at, paid_at, payout_id) FROM stdin;
\.


--
-- Data for Name: affiliate_links; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.affiliate_links (id, user_id, code, name, clicks, conversions, total_revenue, total_commission, commission_rate, is_active, created_at, last_click_at) FROM stdin;
\.


--
-- Data for Name: affiliate_payouts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.affiliate_payouts (id, affiliate_user_id, amount, method, payment_details, status, notes, transaction_id, requested_at, processed_at, completed_at) FROM stdin;
\.


--
-- Data for Name: affiliate_referrals; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.affiliate_referrals (id, affiliate_link_id, affiliate_user_id, referred_user_id, ip_address, user_agent, landing_page, status, program_id, purchase_amount, commission_amount, click_date, conversion_date) FROM stdin;
\.


--
-- Data for Name: affiliate_settings; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.affiliate_settings (id, default_commission_rate, min_payout_amount, cookie_duration_days, is_active, auto_approve_affiliates, auto_approve_commissions, terms_and_conditions, updated_at) FROM stdin;
1	10.00	50.00	30	t	f	f	By participating in the MarketEdgePros Affiliate Program, you agree to promote our services ethically and honestly. Commissions are earned on qualified sales only. Minimum payout is $50. Payments are processed monthly.	2025-10-26 18:36:56.542341
2	10.00	50.00	30	t	f	f	By participating in the MarketEdgePros Affiliate Program, you agree to promote our services ethically and honestly. Commissions are earned on qualified sales only. Minimum payout is $50. Payments are processed monthly.	2025-10-26 20:14:05.886439
3	10.00	50.00	30	t	f	f	By participating in the MarketEdgePros Affiliate Program, you agree to promote our services ethically and honestly. Commissions are earned on qualified sales only. Minimum payout is $50. Payments are processed monthly.	2025-10-26 20:16:50.802038
\.


--
-- Data for Name: agents; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.agents (id, agent_code, user_id, commission_rate, total_earned, total_withdrawn, pending_balance, referral_count, active_referrals, total_sales, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
007_add_performance_indexes
\.


--
-- Data for Name: blog_posts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.blog_posts (id, title, slug, excerpt, content, featured_image, featured_image_alt, category, tags, meta_title, meta_description, meta_keywords, author_id, status, published_at, view_count, featured, reading_time, created_at, updated_at) FROM stdin;
10	What is Prop Trading? A Complete Guide for Beginners	what-is-prop-trading-complete-guide	Discover everything you need to know about proprietary trading, how it works, and why it's becoming the preferred path for aspiring traders worldwide.	# What is Prop Trading?\n\nProprietary trading, commonly known as "prop trading," is when a financial firm or commercial bank uses its own money to trade financial instruments, rather than trading on behalf of clients. In the context of retail prop trading firms like MarketEdgePros, it refers to firms that provide capital to skilled traders to trade on their behalf.\n\n## How Does Prop Trading Work?\n\nThe process is straightforward:\n\n1. **Evaluation Phase**: Traders prove their skills through a challenge or evaluation process\n2. **Funding**: Successful traders receive access to substantial trading capital\n3. **Profit Sharing**: Traders keep a significant portion of the profits they generate (typically 70-90%)\n4. **Risk Management**: The firm sets rules to protect capital while allowing traders freedom to execute their strategies\n\n## Why Choose Prop Trading?\n\n### Access to Capital\nThe biggest advantage is access to substantial trading capital without risking your own money. Instead of trading a $1,000 account, you could be trading $100,000 or more.\n\n### Profit Potential\nWith larger capital comes larger profit potential. A 5% return on $100,000 is $5,000, compared to just $50 on a $1,000 account.\n\n### Professional Development\nProp firms provide professional trading environments, tools, and often mentorship that help traders develop their skills faster.\n\n### Risk Management\nYou're not risking your personal savings. The firm provides the capital and absorbs the losses (within defined parameters).\n\n## Getting Started\n\nTo begin your prop trading journey:\n\n1. **Develop Your Skills**: Practice with a demo account until you're consistently profitable\n2. **Choose a Reputable Firm**: Research firms like MarketEdgePros that offer fair terms and support\n3. **Pass the Evaluation**: Demonstrate your ability to trade profitably while managing risk\n4. **Start Trading**: Once funded, execute your strategy and grow your account\n\nReady to start your prop trading journey? Explore our programs and take the first step toward becoming a funded trader.	/images/blog/prop-trading-guide.jpg	Prop Trading Guide	Education	{"Prop Trading","Beginners Guide","Trading Education","Getting Started"}	What is Prop Trading? Complete Beginner's Guide 2024	Learn everything about proprietary trading, how it works, and how to become a funded trader. Complete guide for beginners.	prop trading, proprietary trading, funded trader, trading capital	77	published	2025-10-19 16:29:46.165526	0	t	5	2025-10-19 16:29:46.165526	2025-10-29 16:29:46.165526
11	5 Key Strategies for Prop Trading Success	5-key-strategies-prop-trading-success	Master these five essential strategies to maximize your success as a proprietary trader and consistently pass funding challenges.	# 5 Key Strategies for Prop Trading Success\n\nSuccess in prop trading requires more than just technical analysis skills. Here are five proven strategies that separate successful funded traders from those who struggle.\n\n## 1. Master Risk Management\n\nRisk management is the foundation of sustainable trading success.\n\n### Key Principles:\n- **Never risk more than 1-2% per trade**: This ensures you can survive losing streaks\n- **Use stop losses religiously**: Every trade should have a predefined exit point\n- **Calculate position sizes carefully**: Use proper position sizing based on your stop loss distance\n- **Respect daily loss limits**: Know when to step away and trade another day\n\n## 2. Develop a Consistent Trading Routine\n\nConsistency is key in prop trading. Successful traders follow a structured routine.\n\n### Morning Routine:\n- Review overnight news and economic calendar\n- Analyze key markets and identify potential setups\n- Set alerts for your watchlist\n- Review your trading plan for the day\n\n## 3. Focus on High-Probability Setups\n\nQuality over quantity is crucial in prop trading.\n\n### Characteristics of High-Probability Setups:\n- **Confluence**: Multiple factors align (support/resistance, trend, indicators)\n- **Clear risk/reward**: Minimum 1:2 risk-reward ratio\n- **Favorable market conditions**: Trading with the trend, during liquid hours\n- **Pattern recognition**: Proven chart patterns with historical success\n\n## 4. Maintain Emotional Discipline\n\nPsychology often determines success more than strategy.\n\n### Mental Game Strategies:\n- **Accept losses as part of the business**: No strategy wins 100% of the time\n- **Don't get emotional about individual trades**: Focus on long-term statistics\n- **Take breaks after losses**: Clear your head before the next trade\n- **Celebrate small wins**: Acknowledge progress and consistency\n\n## 5. Continuous Learning and Adaptation\n\nMarkets evolve, and so should your approach.\n\n### Growth Activities:\n- **Review your trades weekly**: Identify patterns in your wins and losses\n- **Study market conditions**: Understand what environments suit your strategy\n- **Learn from mistakes**: Every loss is a lesson if you analyze it\n- **Stay updated**: Follow market news and adapt to changing conditions\n\nReady to apply these strategies? Start your evaluation and become a funded trader today.	/images/blog/trading-strategies.jpg	Trading Strategies	Strategy	{"Trading Strategies","Risk Management","Trading Psychology","Success Tips"}	5 Key Strategies for Prop Trading Success | Expert Tips	Learn the 5 essential strategies every successful prop trader uses. Master risk management, discipline, and high-probability setups.	trading strategies, prop trading success, risk management, trading discipline	77	published	2025-10-21 16:29:46.165526	0	t	5	2025-10-21 16:29:46.165526	2025-10-29 16:29:46.165526
12	How to Choose the Right Prop Firm: A Comprehensive Guide	how-to-choose-right-prop-firm	Not all prop firms are created equal. Learn the key factors to consider when selecting a proprietary trading firm that aligns with your goals.	# How to Choose the Right Prop Firm\n\nChoosing the right prop firm is one of the most important decisions in your trading journey. With dozens of firms competing for your business, how do you separate the legitimate opportunities from the rest?\n\n## Key Factors to Consider\n\n### 1. Profit Split\n\nThe profit split determines how much of your trading profits you keep.\n\n**What to Look For:**\n- **Competitive splits**: 70-90% is standard\n- **Scaling opportunities**: Can you increase your split over time?\n- **Transparency**: Are there hidden fees that reduce your actual take-home?\n\n### 2. Trading Rules and Restrictions\n\nRules protect the firm's capital, but they should also be achievable.\n\n**Evaluate:**\n- **Daily loss limits**: Are they reasonable for your strategy?\n- **Maximum drawdown**: Can you trade comfortably within these limits?\n- **Profit targets**: Are they realistic and achievable?\n- **Trading restrictions**: What instruments, times, or strategies are allowed?\n\n### 3. Payout Process\n\nGetting paid should be straightforward and reliable.\n\n**Questions to Ask:**\n- How often can you request payouts?\n- What's the minimum payout amount?\n- How long does processing take?\n- What payment methods are available?\n- Are there payout fees?\n\n### 4. Reputation and Track Record\n\nA firm's reputation speaks volumes.\n\n**Research:**\n- **Online reviews**: Check Trustpilot, Reddit, and trading forums\n- **Social proof**: Look for verified trader testimonials\n- **Company history**: How long have they been in business?\n- **Transparency**: Do they share statistics about funded traders?\n\n## Why MarketEdgePros Stands Out\n\nAt MarketEdgePros, we've built our reputation on:\n\n- **90% profit split**: Industry-leading profit sharing\n- **No time limits**: Trade at your own pace\n- **Fast payouts**: Request withdrawals anytime\n- **Realistic targets**: Achievable profit goals\n- **24/7 support**: Always here to help\n- **Transparent rules**: No hidden surprises\n\nReady to experience the MarketEdgePros difference? Explore our programs and start your funded trading journey today.	/images/blog/choose-prop-firm.jpg	Choosing a Prop Firm	Education	{"Prop Firms","Choosing a Firm","Trading Education","Due Diligence"}	How to Choose the Right Prop Firm | Complete Guide 2024	Learn how to evaluate and choose the best prop trading firm. Compare profit splits, rules, payouts, and reputation to find your perfect match.	prop firm comparison, choose prop firm, best prop firms, prop trading firms	77	published	2025-10-23 16:29:46.165526	0	f	5	2025-10-23 16:29:46.165526	2025-10-29 16:29:46.165526
13	A Day in the Life of a Successful Prop Trader	day-in-life-successful-prop-trader	Ever wondered what a typical day looks like for a funded proprietary trader? Get an inside look at the daily routine, challenges, and rewards.	# A Day in the Life of a Successful Prop Trader\n\nWhat does it really take to succeed as a funded prop trader? Let's follow a successful trader managing a $200,000 funded account through a typical trading day.\n\n## 5:30 AM - Morning Preparation\n\nThe day starts before the markets open. Trading success begins with preparation.\n\n**Morning Routine:**\n- Quick review of overnight market movements\n- Check economic calendar for major news events\n- Scan for any geopolitical developments\n- Review yesterday's trades and notes\n\n## 8:00 AM - Trading Plan\n\nBefore placing any trades, create a clear plan.\n\n**Today's Plan:**\n- Maximum 3 trades\n- Risk per trade: 1% ($2,000 per trade)\n- Target: 2% account growth ($4,000)\n- Focus: Trend continuation setups\n\n## 9:00 AM - Market Open\n\nThe London session brings liquidity and opportunity.\n\n**First Trade Setup:**\n- **Pair**: EUR/USD\n- **Setup**: Bullish continuation after pullback\n- **Risk/Reward**: 1:2\n- **Position Size**: Calculated for 1% risk\n\n## 12:00 PM - Lunch Break\n\nTake a proper lunch break away from screens. Trading is mentally demanding. Regular breaks maintain focus and prevent emotional decisions.\n\n## 4:00 PM - Trade Review\n\n**Daily Results:**\n- Trades taken: 2\n- Win rate: 50%\n- Net profit: $4,000 (2% account growth)\n- Rules followed: 100%\n\n## 5:00 PM - End of Day Routine\n\nWrap up with essential admin tasks.\n\n**End of Day Checklist:**\n- Update trading journal with detailed notes\n- Screenshot all trades for records\n- Review what worked and what didn't\n- Prepare watchlist for tomorrow\n\n## Key Takeaways\n\nSuccess as a prop trader requires:\n\n1. **Preparation**: Start each day with a clear plan\n2. **Discipline**: Follow your rules religiously\n3. **Patience**: Wait for high-probability setups\n4. **Management**: Protect profits with proper trade management\n5. **Balance**: Maintain life outside of trading\n\nReady to start your own funded trading journey? Explore MarketEdgePros programs and take the first step.	/images/blog/trader-lifestyle.jpg	Prop Trader Lifestyle	Lifestyle	{"Day Trading","Trading Routine","Prop Trader Life","Trading Discipline"}	A Day in the Life of a Successful Prop Trader | Real Routine	Follow a funded prop trader through their daily routine. Learn the habits, discipline, and strategies that lead to consistent trading success.	prop trader routine, day in the life, trading lifestyle, funded trader	77	published	2025-10-25 16:29:46.165526	0	f	5	2025-10-25 16:29:46.165526	2025-10-29 16:29:46.165526
14	Risk Management in Prop Trading: The Ultimate Guide	risk-management-prop-trading-guide	Risk management is the difference between long-term success and account blowouts. Master these essential risk management principles for prop trading.	# Risk Management in Prop Trading: The Ultimate Guide\n\nRisk management isn't just important in prop trading—it's everything. The best strategy in the world won't save you if you can't manage risk properly.\n\n## Why Risk Management Matters More in Prop Trading\n\nIn prop trading, you're not just managing your own money—you're managing the firm's capital with strict rules.\n\n**The Reality:**\n- One bad day can end your funded account\n- Daily loss limits are non-negotiable\n- Maximum drawdown rules must be respected\n- Consistency matters more than big wins\n\n**The Goal:**\nPreserve capital first, make profits second.\n\n## The 1% Rule: Your Foundation\n\nThe most fundamental risk management principle: never risk more than 1% of your account on a single trade.\n\n### Why 1%?\n\n**Math Doesn't Lie:**\n- With 1% risk, you can survive 100 consecutive losses\n- With 5% risk, you're out after 20 losses\n- With 10% risk, you're done after 10 losses\n\n## Daily Loss Limits: Your Safety Net\n\nMost prop firms enforce daily loss limits (typically 3-5% of account balance).\n\n### Managing Daily Risk\n\n**Strategy:**\n- If daily limit is 5%, risk only 1% per trade\n- This gives you 5 attempts before hitting the limit\n- Stop trading if you lose 2 trades in a row\n- Reset mentally before trading again\n\n## Position Sizing: The Critical Calculation\n\nProper position sizing ensures you risk exactly what you intend.\n\n### The Formula\n\n**For Forex:**\n```\nLot Size = (Account Balance × Risk %) / (Stop Loss in Pips × Pip Value)\n```\n\n## Risk/Reward Ratios: Making Math Work For You\n\nYour risk/reward ratio determines how often you need to win to be profitable.\n\n### The Math\n\n**1:2 Risk/Reward:**\n- Need 33%+ win rate to profit\n- Even 40% win rate is profitable\n\n**Example:**\n- 10 trades, 40% win rate (4 wins, 6 losses)\n- Losses: 6 × $1,000 = -$6,000\n- Wins: 4 × $2,000 = +$8,000\n- Net: +$2,000 profit\n\n## The Bottom Line\n\n**Risk management is not optional in prop trading—it's mandatory.**\n\n**Remember:**\n- Protect capital first\n- Profits come from consistency, not home runs\n- One bad trade shouldn't end your account\n- Follow your rules even when it's hard\n\nReady to apply professional risk management with real capital? Explore MarketEdgePros programs and start trading with proper risk management from day one.	/images/blog/risk-management.jpg	Risk Management	Risk Management	{"Risk Management","Position Sizing","Trading Rules","Capital Preservation"}	Risk Management in Prop Trading | Complete Guide 2024	Master risk management for prop trading. Learn position sizing, drawdown management, and the rules that protect your funded account.	risk management, prop trading risk, position sizing, drawdown management	77	published	2025-10-27 16:29:46.165526	0	f	5	2025-10-27 16:29:46.165526	2025-10-29 16:29:46.165526
7	5 Essential Risk Management Strategies for Prop Traders	5-essential-risk-management-strategies-for-prop-traders	Learn the top 5 risk management strategies that every successful prop trader must master to protect their capital and maximize profits.	<h2>Introduction</h2><p>Risk management is the cornerstone of successful prop trading.</p>	\N	\N	risk_management	risk management, prop trading, trading strategies, position sizing	\N	\N	\N	78	published	2025-10-19 14:20:45.605918	8	t	8	2025-10-26 14:20:45.605918	2025-10-29 16:41:36.833085
8	How to Pass Your First Prop Firm Challenge	how-to-pass-your-first-prop-firm-challenge	A complete step-by-step guide to successfully passing your first prop firm challenge and becoming a funded trader.	<h2>Understanding the Challenge</h2><p>Prop firm challenges are designed to test your trading skills.</p>	\N	\N	prop_trading	prop trading, funded trader, trading challenge, prop firm	\N	\N	\N	78	published	2025-10-21 14:20:45.605918	22	t	10	2025-10-26 14:20:45.605918	2025-10-29 18:10:48.158995
\.


--
-- Data for Name: challenges; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.challenges (id, user_id, program_id, status, start_date, end_date, passed_at, account_number, initial_balance, current_balance, total_profit, total_loss, max_drawdown, current_phase, total_phases, payment_status, payment_id, addons, created_at, updated_at, created_by, payment_type, approval_status, approved_by, approved_at, rejection_reason) FROM stdin;
\.


--
-- Data for Name: commission_balances; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.commission_balances (id, user_id, total_earned, available_balance, pending_balance, withdrawn_total, total_commissions, last_commission_at, last_withdrawal_at, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: commission_rules; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.commission_rules (id, name, description, rule_type, target_role, level_1_rate, level_2_rate, level_3_rate, level_4_rate, level_5_rate, max_levels, is_active, min_amount, max_amount, created_at, updated_at) FROM stdin;
1	Agent - Program Purchase	Commission for agents on program purchases	program_purchase	agent	10.00	5.00	2.00	0.00	0.00	3	t	0.00	\N	2025-10-21 17:39:26.818567	2025-10-21 17:39:26.818567
2	Agent - Trading Profit	Commission for agents on trading profits	trading_profit	agent	5.00	2.00	0.00	0.00	0.00	2	t	0.00	\N	2025-10-21 17:39:26.818567	2025-10-21 17:39:26.818567
3	Master - Program Purchase	Commission for masters on program purchases	program_purchase	master	15.00	10.00	5.00	2.00	0.00	4	t	0.00	\N	2025-10-21 17:39:26.907412	2025-10-21 17:39:26.907412
4	Master - Trading Profit	Commission for masters on trading profits	trading_profit	master	7.00	5.00	2.00	0.00	0.00	3	t	0.00	\N	2025-10-21 17:39:26.907412	2025-10-21 17:39:26.907412
5	Supermaster - Program Purchase	Commission for supermasters on program purchases	program_purchase	supermaster	20.00	15.00	10.00	5.00	2.00	5	t	0.00	\N	2025-10-21 17:39:26.995585	2025-10-21 17:39:26.995585
6	Supermaster - Trading Profit	Commission for supermasters on trading profits	trading_profit	supermaster	10.00	7.00	5.00	2.00	0.00	4	t	0.00	\N	2025-10-21 17:39:26.995585	2025-10-21 17:39:26.995585
\.


--
-- Data for Name: commission_withdrawals; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.commission_withdrawals (id, user_id, amount, currency, payment_method, payment_details, status, requested_at, approved_at, approved_by, completed_at, rejected_at, rejection_reason, transaction_reference, notes, admin_notes, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: commissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.commissions (id, agent_id, referral_id, challenge_id, sale_amount, commission_rate, commission_amount, status, approved_at, paid_at, payment_method, transaction_id, created_at, updated_at, user_id, source_type, source_id, source_user_id, rule_id, level, base_amount, approved_by, payment_reference, notes, admin_notes) FROM stdin;
\.


--
-- Data for Name: course_enrollments; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.course_enrollments (id, email, name, enrolled_at, module_1_sent, module_1_sent_at, module_2_sent, module_2_sent_at, module_3_sent, module_3_sent_at, module_4_sent, module_4_sent_at, module_5_sent, module_5_sent_at, last_email_opened_at, unsubscribed, unsubscribed_at, created_at, updated_at) FROM stdin;
1	benga1113@gmail.com	ben gabay	2025-10-26 12:21:44.685439	f	\N	f	\N	f	\N	f	\N	f	\N	\N	f	\N	2025-10-26 12:21:44.685451	2025-10-26 12:21:44.685454
2	test3@example.com	John Doe	2025-10-26 12:22:42.000309	f	\N	f	\N	f	\N	f	\N	f	\N	\N	f	\N	2025-10-26 12:22:42.000322	2025-10-26 12:22:42.000326
3	test4@example.com	Jane Smith	2025-10-26 12:24:10.017266	f	\N	f	\N	f	\N	f	\N	f	\N	\N	f	\N	2025-10-26 12:24:10.017279	2025-10-26 12:24:10.017282
4	bengab1113@gmail.com	ben gabay	2025-10-26 12:25:03.549672	f	\N	f	\N	f	\N	f	\N	f	\N	\N	f	\N	2025-10-26 12:25:03.549684	2025-10-26 12:25:03.549688
\.


--
-- Data for Name: email_queue; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.email_queue (id, user_id, to_email, subject, body, html_body, status, attempts, max_attempts, error_message, sent_at, created_at, updated_at) FROM stdin;
1	102	gabay037@gmail.com	Verify Your Email - MarketEdgePros		\n        <html>\n            <body>\n                <h2>Welcome to MarketEdgePros!</h2>\n                <p>Hi liav,</p>\n                <p>Please verify your email address by clicking the link below:</p>\n                <p><a href="https://marketedgepros.com/verify-email?token=-0JrpAx3PRVCIQH2U66F6absPmdncYXunuG8Fiw_aTE">Verify Email</a></p>\n                <p>Or copy this link: https://marketedgepros.com/verify-email?token=-0JrpAx3PRVCIQH2U66F6absPmdncYXunuG8Fiw_aTE</p>\n                <p>Best regards,  \nMarketEdgePros Team</p>\n            </body>\n        </html>\n        	sent	0	3	HTTP Error 403: Forbidden	2025-10-27 23:33:22.627175	2025-10-27 23:05:03.568272	2025-10-27 23:33:22.63018
\.


--
-- Data for Name: email_verification_tokens; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.email_verification_tokens (id, user_id, code, token, expires_at, used, created_at, updated_at) FROM stdin;
12	102	368255	GG-ZGHRVLCc6gQeY7MmpCDPqmV5wFPVa9THiqd9hTRs	2025-10-28 18:50:36.062088	f	2025-10-27 18:50:36.064881	2025-10-27 18:50:36.06489
13	103	578598	6zId6R6Zs5Bitc3HhIC1IxYAqRGnrirfdcv_NkQeXFs	2025-10-30 07:26:39.642055	t	2025-10-29 07:26:39.643599	2025-10-29 07:27:42.670134
\.


--
-- Data for Name: faqs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.faqs (id, question, answer, category, "order", is_featured, is_published, view_count, helpful_count, not_helpful_count, created_at, updated_at) FROM stdin;
2	What are the trading rules for prop firm challenges?	<p>Our challenges have clear and fair rules:</p><ul><li><strong>Daily Loss Limit:</strong> Maximum 5% loss per day</li><li><strong>Max Drawdown:</strong> 10% total drawdown limit</li><li><strong>Profit Target:</strong> 8-10% depending on your program</li><li><strong>Trading Days:</strong> Minimum 5 trading days required</li><li><strong>Allowed Instruments:</strong> Forex, indices, commodities, and crypto</li></ul><p>Always trade within the rules to ensure your challenge success!</p>	trading	2	t	t	0	0	0	2025-10-26 14:44:11.026434	2025-10-26 14:44:11.026434
3	How long does KYC verification take?	<p>KYC verification typically takes 24-48 hours. To speed up the process:</p><ul><li>Upload clear, high-quality documents</li><li>Ensure all information matches your ID exactly</li><li>Provide both proof of identity and proof of address</li></ul><p>You'll receive an email once your verification is complete.</p>	account	3	t	t	0	0	0	2025-10-26 14:44:11.026434	2025-10-26 14:44:11.026434
4	When can I withdraw my profits?	<p>Profit withdrawals are available:</p><ul><li><strong>First Payout:</strong> After 14 days of funded trading</li><li><strong>Regular Payouts:</strong> Bi-weekly (every 2 weeks)</li><li><strong>Processing Time:</strong> 1-3 business days</li><li><strong>Methods:</strong> Bank transfer, crypto, or e-wallet</li></ul><p>Minimum withdrawal amount is $100.</p>	payments	4	t	t	0	0	0	2025-10-26 14:44:11.026434	2025-10-26 14:44:11.026434
5	What payment methods do you accept?	<p>We accept multiple payment methods for your convenience:</p><ul><li>Credit/Debit Cards (Visa, Mastercard)</li><li>Cryptocurrency (Bitcoin, Ethereum, USDT)</li><li>Bank Transfer</li><li>E-wallets (PayPal, Skrill, Neteller)</li></ul><p>All payments are processed securely through our payment partners.</p>	payments	5	f	t	0	0	0	2025-10-26 14:44:11.026434	2025-10-26 14:44:11.026434
6	Can I use Expert Advisors (EAs) or trading bots?	<p>Yes! You can use Expert Advisors and trading bots with these conditions:</p><ul><li>No high-frequency scalping (HFT)</li><li>No tick scalping or arbitrage strategies</li><li>No copy trading from external sources</li><li>All trading must comply with our risk rules</li></ul><p>If you're unsure about your EA, contact support before using it.</p>	trading	6	f	t	0	0	0	2025-10-26 14:44:11.026434	2025-10-26 14:44:11.026434
7	What happens if I fail my challenge?	<p>Don't worry! Failing a challenge is a learning opportunity:</p><ul><li>You can purchase a new challenge at any time</li><li>We offer discount codes for retry attempts</li><li>Review your trading statistics to improve</li><li>Consider our free trading course for better preparation</li></ul><p>Many successful traders fail their first attempt - persistence is key!</p>	trading	7	f	t	0	0	0	2025-10-26 14:44:11.026434	2025-10-26 14:44:11.026434
8	How do I reset my password?	<p>To reset your password:</p><ol><li>Go to the login page</li><li>Click "Forgot Password"</li><li>Enter your registered email address</li><li>Check your email for the reset link</li><li>Follow the link and create a new password</li></ol><p>If you don't receive the email within 5 minutes, check your spam folder or contact support.</p>	account	8	f	t	0	0	0	2025-10-26 14:44:11.026434	2025-10-26 14:44:11.026434
9	Is my trading data and personal information secure?	<p>Absolutely! We take security seriously:</p><ul><li>SSL encryption for all data transmission</li><li>Secure database storage with regular backups</li><li>Compliance with GDPR and data protection laws</li><li>Two-factor authentication (2FA) available</li><li>Regular security audits and updates</li></ul><p>Your data is never shared with third parties without your consent.</p>	technical	9	f	t	0	0	0	2025-10-26 14:44:11.026434	2025-10-26 14:44:11.026434
10	Can I trade during news events?	<p>Yes, you can trade during news events, but be cautious:</p><ul><li>High volatility can lead to rapid losses</li><li>Spreads may widen significantly</li><li>Ensure you have proper risk management in place</li><li>Consider avoiding major news if you're close to your limits</li></ul><p>Many successful traders avoid high-impact news to protect their accounts.</p>	trading	10	f	t	0	0	0	2025-10-26 14:44:11.026434	2025-10-26 14:44:11.026434
1	How do I get started with MarketEdgePros?	<p>Getting started is easy! Follow these steps:</p><ol><li>Create your free account</li><li>Complete your profile and KYC verification</li><li>Choose a challenge program that fits your goals</li><li>Make your payment and receive your trading credentials</li><li>Start trading and pass your evaluation!</li></ol><p>Need help? Our support team is here 24/7.</p>	getting_started	1	t	t	0	1	0	2025-10-26 14:44:11.026434	2025-10-27 12:13:17.740973
\.


--
-- Data for Name: lead_activities; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.lead_activities (id, lead_id, user_id, activity_type, subject, description, outcome, scheduled_at, completed, completed_at, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: lead_notes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.lead_notes (id, lead_id, user_id, content, is_important, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: leads; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.leads (id, first_name, last_name, email, phone, country_code, status, source, score, assigned_to, assigned_at, interested_program_id, budget, converted_to_user_id, converted_at, lost_reason, lost_notes, lost_at, company, job_title, notes, tags, last_contacted_at, next_follow_up, created_at, updated_at) FROM stdin;
1	ben	gabay	benga1113@gmail.com	\N	\N	new	free_course	0	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2025-10-26 12:21:44.673979	2025-10-26 12:21:44.67399
2	John	Doe	test3@example.com	\N	\N	new	free_course	0	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2025-10-26 12:22:41.995942	2025-10-26 12:22:41.995953
3	Jane	Smith	test4@example.com	\N	\N	new	free_course	0	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2025-10-26 12:24:10.006325	2025-10-26 12:24:10.006337
4	ben	gabay	bengab1113@gmail.com	\N	\N	new	free_course	0	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2025-10-26 12:25:03.541852	2025-10-26 12:25:03.541864
\.


--
-- Data for Name: notification_preferences; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.notification_preferences (id, user_id, in_app_withdrawal, in_app_commission, in_app_kyc, in_app_system, in_app_payment, in_app_challenge, email_withdrawal, email_commission, email_kyc, email_system, email_payment, email_challenge, email_enabled, email_frequency, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.notifications (id, user_id, type, title, message, data, priority, is_read, read_at, is_deleted, deleted_at, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: password_reset_tokens; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.password_reset_tokens (id, user_id, code, token, expires_at, used, created_at, updated_at) FROM stdin;
1	103	599170	t4KTlt--cRpK3q-X75iuvL5sKT0yX7qc3RaKFSJs4ng	2025-10-30 11:54:10.35121	t	2025-10-30 11:39:10.354383	2025-10-30 11:39:41.283544
\.


--
-- Data for Name: payment_approval_requests; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.payment_approval_requests (id, challenge_id, payment_id, requested_by, requested_for, amount, payment_type, status, reviewed_by, reviewed_at, rejection_reason, admin_notes, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.payments (id, user_id, amount, currency, payment_method, transaction_id, status, purpose, reference_id, provider_response, created_at, updated_at, completed_at, payment_type, approval_status, approved_by, approved_at, rejection_reason, admin_notes) FROM stdin;
\.


--
-- Data for Name: program_addons; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.program_addons (id, program_id, name, description, price, price_type, benefits, is_active, created_at, updated_at) FROM stdin;
1	29	Increased Leverage	Trade with higher leverage for greater profit potential	75.00	fixed	{"leverage": "1:100", "description": "Increase your leverage from 1:30 to 1:100"}	t	2025-10-29 23:11:26.621788	2025-10-29 23:11:26.621796
2	29	90% Profit Split	Keep 90% of your profits instead of 80%	100.00	fixed	{"description": "Earn an extra 10% on all your profits", "profit_split": "90%"}	t	2025-10-29 23:11:26.621799	2025-10-29 23:11:26.621801
3	29	Bi-weekly Payouts	Get paid every 2 weeks instead of monthly	50.00	fixed	{"description": "Receive your profits twice as often", "payout_frequency": "Bi-weekly"}	t	2025-10-29 23:11:26.621803	2025-10-29 23:11:26.621805
4	29	No Minimum Trading Days	Remove the minimum trading days requirement	30.00	fixed	{"min_days": "0", "description": "Trade whenever you want, no minimum days required"}	t	2025-10-29 23:11:26.621807	2025-10-29 23:11:26.621809
5	24	Increased Leverage	Trade with higher leverage for greater profit potential	75.00	fixed	{"leverage": "1:100", "description": "Increase your leverage from 1:30 to 1:100"}	t	2025-10-29 23:11:26.627653	2025-10-29 23:11:26.627659
6	24	90% Profit Split	Keep 90% of your profits instead of 80%	100.00	fixed	{"description": "Earn an extra 10% on all your profits", "profit_split": "90%"}	t	2025-10-29 23:11:26.627661	2025-10-29 23:11:26.627663
7	24	Bi-weekly Payouts	Get paid every 2 weeks instead of monthly	50.00	fixed	{"description": "Receive your profits twice as often", "payout_frequency": "Bi-weekly"}	t	2025-10-29 23:11:26.627665	2025-10-29 23:11:26.627666
8	24	No Minimum Trading Days	Remove the minimum trading days requirement	30.00	fixed	{"min_days": "0", "description": "Trade whenever you want, no minimum days required"}	t	2025-10-29 23:11:26.627668	2025-10-29 23:11:26.62767
9	25	Increased Leverage	Trade with higher leverage for greater profit potential	75.00	fixed	{"leverage": "1:100", "description": "Increase your leverage from 1:30 to 1:100"}	t	2025-10-29 23:11:26.631802	2025-10-29 23:11:26.631807
10	25	90% Profit Split	Keep 90% of your profits instead of 80%	100.00	fixed	{"description": "Earn an extra 10% on all your profits", "profit_split": "90%"}	t	2025-10-29 23:11:26.631809	2025-10-29 23:11:26.631811
11	25	Bi-weekly Payouts	Get paid every 2 weeks instead of monthly	50.00	fixed	{"description": "Receive your profits twice as often", "payout_frequency": "Bi-weekly"}	t	2025-10-29 23:11:26.631813	2025-10-29 23:11:26.631814
12	25	No Minimum Trading Days	Remove the minimum trading days requirement	30.00	fixed	{"min_days": "0", "description": "Trade whenever you want, no minimum days required"}	t	2025-10-29 23:11:26.631816	2025-10-29 23:11:26.631818
13	26	Increased Leverage	Trade with higher leverage for greater profit potential	75.00	fixed	{"leverage": "1:100", "description": "Increase your leverage from 1:30 to 1:100"}	t	2025-10-29 23:11:26.635593	2025-10-29 23:11:26.635598
14	26	90% Profit Split	Keep 90% of your profits instead of 80%	100.00	fixed	{"description": "Earn an extra 10% on all your profits", "profit_split": "90%"}	t	2025-10-29 23:11:26.6356	2025-10-29 23:11:26.635602
15	26	Bi-weekly Payouts	Get paid every 2 weeks instead of monthly	50.00	fixed	{"description": "Receive your profits twice as often", "payout_frequency": "Bi-weekly"}	t	2025-10-29 23:11:26.635604	2025-10-29 23:11:26.635606
16	26	No Minimum Trading Days	Remove the minimum trading days requirement	30.00	fixed	{"min_days": "0", "description": "Trade whenever you want, no minimum days required"}	t	2025-10-29 23:11:26.635607	2025-10-29 23:11:26.635609
17	27	Increased Leverage	Trade with higher leverage for greater profit potential	75.00	fixed	{"leverage": "1:100", "description": "Increase your leverage from 1:30 to 1:100"}	t	2025-10-29 23:11:26.639202	2025-10-29 23:11:26.639208
18	27	90% Profit Split	Keep 90% of your profits instead of 80%	100.00	fixed	{"description": "Earn an extra 10% on all your profits", "profit_split": "90%"}	t	2025-10-29 23:11:26.639211	2025-10-29 23:11:26.639212
19	27	Bi-weekly Payouts	Get paid every 2 weeks instead of monthly	50.00	fixed	{"description": "Receive your profits twice as often", "payout_frequency": "Bi-weekly"}	t	2025-10-29 23:11:26.639214	2025-10-29 23:11:26.639216
20	27	No Minimum Trading Days	Remove the minimum trading days requirement	30.00	fixed	{"min_days": "0", "description": "Trade whenever you want, no minimum days required"}	t	2025-10-29 23:11:26.639218	2025-10-29 23:11:26.639219
21	28	Increased Leverage	Trade with higher leverage for greater profit potential	75.00	fixed	{"leverage": "1:100", "description": "Increase your leverage from 1:30 to 1:100"}	t	2025-10-29 23:11:26.642845	2025-10-29 23:11:26.64285
22	28	90% Profit Split	Keep 90% of your profits instead of 80%	100.00	fixed	{"description": "Earn an extra 10% on all your profits", "profit_split": "90%"}	t	2025-10-29 23:11:26.642852	2025-10-29 23:11:26.642854
23	28	Bi-weekly Payouts	Get paid every 2 weeks instead of monthly	50.00	fixed	{"description": "Receive your profits twice as often", "payout_frequency": "Bi-weekly"}	t	2025-10-29 23:11:26.642855	2025-10-29 23:11:26.642857
24	28	No Minimum Trading Days	Remove the minimum trading days requirement	30.00	fixed	{"min_days": "0", "description": "Trade whenever you want, no minimum days required"}	t	2025-10-29 23:11:26.642859	2025-10-29 23:11:26.642861
25	30	Increased Leverage	Trade with higher leverage for greater profit potential	75.00	fixed	{"leverage": "1:100", "description": "Increase your leverage from 1:30 to 1:100"}	t	2025-10-29 23:11:26.646702	2025-10-29 23:11:26.646709
26	30	90% Profit Split	Keep 90% of your profits instead of 80%	100.00	fixed	{"description": "Earn an extra 10% on all your profits", "profit_split": "90%"}	t	2025-10-29 23:11:26.646713	2025-10-29 23:11:26.646716
27	30	Bi-weekly Payouts	Get paid every 2 weeks instead of monthly	50.00	fixed	{"description": "Receive your profits twice as often", "payout_frequency": "Bi-weekly"}	t	2025-10-29 23:11:26.64672	2025-10-29 23:11:26.646723
28	30	No Minimum Trading Days	Remove the minimum trading days requirement	30.00	fixed	{"min_days": "0", "description": "Trade whenever you want, no minimum days required"}	t	2025-10-29 23:11:26.646726	2025-10-29 23:11:26.646729
29	37	Increased Leverage	Trade with higher leverage for greater profit potential	75.00	fixed	{"leverage": "1:100", "description": "Increase your leverage from 1:30 to 1:100"}	t	2025-10-29 23:11:26.650699	2025-10-29 23:11:26.650707
30	37	90% Profit Split	Keep 90% of your profits instead of 80%	100.00	fixed	{"description": "Earn an extra 10% on all your profits", "profit_split": "90%"}	t	2025-10-29 23:11:26.650711	2025-10-29 23:11:26.650714
31	37	Bi-weekly Payouts	Get paid every 2 weeks instead of monthly	50.00	fixed	{"description": "Receive your profits twice as often", "payout_frequency": "Bi-weekly"}	t	2025-10-29 23:11:26.650717	2025-10-29 23:11:26.65072
32	37	No Minimum Trading Days	Remove the minimum trading days requirement	30.00	fixed	{"min_days": "0", "description": "Trade whenever you want, no minimum days required"}	t	2025-10-29 23:11:26.650723	2025-10-29 23:11:26.650726
\.


--
-- Data for Name: referrals; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.referrals (id, agent_id, referred_user_id, referral_code, ip_address, user_agent, status, first_purchase_at, total_purchases, total_spent, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.roles (id, name, label, label_he, color, icon, hierarchy, permissions, is_active, created_at, updated_at) FROM stdin;
1	supermaster	Super Master	סופר מנהל	bg-purple-100 text-purple-800	👑	1	{"can_create_users": true, "can_create_without_verification": true, "can_manage_commissions": true, "can_view_all_users": true, "can_delete_users": true, "can_manage_programs": true, "can_manage_payments": true, "can_manage_roles": true}	t	2025-10-22 22:50:42.486679	2025-10-22 22:50:42.48669
2	super_admin	Super Admin	מנהל על	bg-purple-100 text-purple-800	👑	1	{"can_create_users": true, "can_create_without_verification": true, "can_manage_commissions": true, "can_view_all_users": true, "can_delete_users": true, "can_manage_programs": true, "can_manage_payments": true, "can_manage_roles": true}	t	2025-10-22 22:50:42.493547	2025-10-22 22:50:42.493556
3	admin	Master	מנהל	bg-blue-100 text-blue-800	⭐	2	{"can_create_users": true, "can_create_without_verification": false, "can_manage_commissions": false, "can_view_all_users": false, "can_delete_users": false, "can_manage_programs": false, "can_manage_payments": false, "can_manage_roles": false}	t	2025-10-22 22:50:42.49848	2025-10-22 22:50:42.498488
4	agent	Agent	סוכן	bg-green-100 text-green-800	🤝	3	{"can_create_users": false, "can_create_without_verification": false, "can_manage_commissions": false, "can_view_all_users": false, "can_delete_users": false, "can_manage_programs": false, "can_manage_payments": false, "can_manage_roles": false}	t	2025-10-22 22:50:42.502621	2025-10-22 22:50:42.502632
5	trader	Trader	משתמש	bg-gray-100 text-gray-800	📊	4	{"can_create_users": false, "can_create_without_verification": false, "can_manage_commissions": false, "can_view_all_users": false, "can_delete_users": false, "can_manage_programs": false, "can_manage_payments": false, "can_manage_roles": false}	t	2025-10-22 22:50:42.506094	2025-10-22 22:50:42.506105
\.


--
-- Data for Name: support_articles; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.support_articles (id, title, slug, content, excerpt, category, subcategory, tags, meta_description, meta_keywords, status, published_at, author_id, views, helpful_count, not_helpful_count, "order", featured, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: support_tickets; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.support_tickets (id, ticket_number, user_id, email, name, subject, description, category, priority, status, assigned_to, attachments, first_response_at, resolved_at, closed_at, rating, feedback, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: tenants; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tenants (id, name, subdomain, custom_domain, status, tier, parent_id, logo_url, favicon_url, primary_color, secondary_color, accent_color, custom_css, settings, contact_email, contact_phone, created_at, updated_at) FROM stdin;
6	MarketEdgePros	main	marketedgepros.com	active	basic	\N	https://marketedgepros-storage.ams3.digitaloceanspaces.com/tenants/main/logo.png	\N	#6366f1	#8b5cf6	#ff6b35	\N	{}	\N	\N	2025-10-20 13:49:16.851188	2025-10-20 13:49:16.851195
7	PropTrade Elite	elite	proptradeelite.com	active	basic	\N	https://marketedgepros-storage.ams3.digitaloceanspaces.com/tenants/elite/logo.png	\N	#3b82f6	#06b6d4	#ff6b35	\N	{}	\N	\N	2025-10-20 13:49:16.851198	2025-10-20 13:49:16.8512
\.


--
-- Data for Name: ticket_messages; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ticket_messages (id, ticket_id, user_id, email, name, message, is_staff, is_internal, attachments, created_at) FROM stdin;
\.


--
-- Data for Name: trades; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trades (id, challenge_id, ticket, symbol, trade_type, volume, open_price, close_price, stop_loss, take_profit, profit, commission, swap, status, open_time, close_time, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: trading_programs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trading_programs (id, tenant_id, name, type, description, account_size, profit_target, max_daily_loss, max_total_loss, price, profit_split, rules, is_active, created_at, updated_at) FROM stdin;
12	6	Instant $10K	instant_funding	Get funded instantly with $10,000 capital. Start trading immediately with no evaluation required.	10000.00	0.00	5.00	10.00	449.00	80.00	{}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
13	6	Instant $15K	instant_funding	Get funded instantly with $15,000 capital. Start trading immediately with no evaluation required.	15000.00	0.00	5.00	10.00	599.00	80.00	{}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
14	6	Instant $25K	instant_funding	Get funded instantly with $25,000 capital. Start trading immediately with no evaluation required.	25000.00	0.00	5.00	10.00	899.00	80.00	{}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
15	6	Instant $50K	instant_funding	Get funded instantly with $50,000 capital. Start trading immediately with no evaluation required.	50000.00	0.00	5.00	10.00	1599.00	80.00	{}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
16	6	One Phase $10K	one_phase	Single-phase evaluation with $10,000 capital. Achieve 8% profit target to get funded.	10000.00	8.00	5.00	10.00	75.00	80.00	{"trading_period_days": 30}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
17	6	One Phase $15K	one_phase	Single-phase evaluation with $15,000 capital. Achieve 8% profit target to get funded.	15000.00	8.00	5.00	10.00	99.00	80.00	{"trading_period_days": 30}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
18	6	One Phase $25K	one_phase	Single-phase evaluation with $25,000 capital. Achieve 8% profit target to get funded.	25000.00	8.00	5.00	10.00	175.00	80.00	{"trading_period_days": 30}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
19	6	One Phase $50K	one_phase	Single-phase evaluation with $50,000 capital. Achieve 8% profit target to get funded.	50000.00	8.00	5.00	10.00	325.00	80.00	{"trading_period_days": 30}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
20	6	One Phase $100K	one_phase	Single-phase evaluation with $100,000 capital. Achieve 8% profit target to get funded.	100000.00	8.00	5.00	10.00	549.00	80.00	{"trading_period_days": 30}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
21	6	One Phase $200K	one_phase	Single-phase evaluation with $200,000 capital. Achieve 8% profit target to get funded.	200000.00	8.00	5.00	10.00	999.00	80.00	{"trading_period_days": 30}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
22	6	One Phase $400K	one_phase	Single-phase evaluation with $400,000 capital. Achieve 8% profit target to get funded.	400000.00	8.00	5.00	10.00	1799.00	80.00	{"trading_period_days": 30}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
29	6	Two Phase $200K	two_phase	Two-phase evaluation with $200,000 capital. Phase 1: 8% target, Phase 2: 5% target.	200000.00	8.00	5.00	10.00	999.00	80.00	{"phase1_target": 8.0, "phase2_target": 5.0, "trading_period_days": 60}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
31	6	Three Phase $10K	three_phase	Three-phase evaluation with $10,000 capital. Most affordable path to funding.	10000.00	8.00	5.00	10.00	39.00	80.00	{"trading_period_days": 90}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
32	6	Three Phase $25K	three_phase	Three-phase evaluation with $25,000 capital. Most affordable path to funding.	25000.00	8.00	5.00	10.00	99.00	80.00	{"trading_period_days": 90}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
33	6	Three Phase $50K	three_phase	Three-phase evaluation with $50,000 capital. Most affordable path to funding.	50000.00	8.00	5.00	10.00	199.00	80.00	{"trading_period_days": 90}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
34	6	Three Phase $100K	three_phase	Three-phase evaluation with $100,000 capital. Most affordable path to funding.	100000.00	8.00	5.00	10.00	349.00	80.00	{"trading_period_days": 90}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
24	6	Two Phase $10K	two_phase	Two-phase evaluation with $10,000 capital. Phase 1: 8% target, Phase 2: 5% target.	10000.00	8.00	5.00	10.00	99.00	80.00	{"phase1_target": 8.0, "phase2_target": 5.0, "trading_period_days": 60}	t	2025-10-22 15:11:02.463194	2025-10-29 23:05:22.734833
25	6	Two Phase $15K	two_phase	Two-phase evaluation with $15,000 capital. Phase 1: 8% target, Phase 2: 5% target.	15000.00	8.00	5.00	10.00	149.00	80.00	{"phase1_target": 8.0, "phase2_target": 5.0, "trading_period_days": 60}	t	2025-10-22 15:11:02.463194	2025-10-29 23:05:22.73894
26	6	Two Phase $25K	two_phase	Two-phase evaluation with $25,000 capital. Phase 1: 8% target, Phase 2: 5% target.	25000.00	8.00	5.00	10.00	249.00	80.00	{"phase1_target": 8.0, "phase2_target": 5.0, "trading_period_days": 60}	t	2025-10-22 15:11:02.463194	2025-10-29 23:05:22.743004
27	6	Two Phase $50K	two_phase	Two-phase evaluation with $50,000 capital. Phase 1: 8% target, Phase 2: 5% target.	50000.00	8.00	5.00	10.00	399.00	80.00	{"phase1_target": 8.0, "phase2_target": 5.0, "trading_period_days": 60}	t	2025-10-22 15:11:02.463194	2025-10-29 23:05:22.746319
28	6	Two Phase $100K	two_phase	Two-phase evaluation with $100,000 capital. Phase 1: 8% target, Phase 2: 5% target.	100000.00	8.00	5.00	10.00	599.00	80.00	{"phase1_target": 8.0, "phase2_target": 5.0, "trading_period_days": 60}	t	2025-10-22 15:11:02.463194	2025-10-29 23:05:22.749484
30	6	Two Phase $400K	two_phase	Two-phase evaluation with $400,000 capital. Phase 1: 8% target, Phase 2: 5% target.	400000.00	8.00	5.00	10.00	1799.00	80.00	{"phase1_target": 8.0, "phase2_target": 5.0, "trading_period_days": 60}	t	2025-10-22 15:11:02.463194	2025-10-29 23:05:22.754659
35	6	Three Phase $200K	three_phase	Three-phase evaluation with $200,000 capital. Most affordable path to funding.	200000.00	8.00	5.00	10.00	699.00	80.00	{"trading_period_days": 90}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
36	6	Three Phase $400K	three_phase	Three-phase evaluation with $400,000 capital. Most affordable path to funding.	400000.00	8.00	5.00	10.00	1299.00	80.00	{"trading_period_days": 90}	t	2025-10-22 15:11:02.463194	2025-10-22 15:11:02.463194
37	6	Two Phase $300K	two_phase	Two-phase evaluation program for $300,000 account	300000.00	10.00	5.00	10.00	1299.00	90.00	{"platforms": ["MT4", "MT5"], "instruments": ["Forex", "Indices", "Commodities"], "max_trading_days": null, "min_trading_days": 4}	t	2025-10-29 23:05:22.761365	2025-10-29 23:05:22.761374
\.


--
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.transactions (id, wallet_id, type, amount, balance_type, balance_before, balance_after, reference_type, reference_id, description, notes, created_by, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, email, password_hash, first_name, last_name, phone, country_code, date_of_birth, avatar_url, is_active, is_verified, email_verified_at, two_factor_enabled, two_factor_secret, kyc_status, kyc_submitted_at, kyc_verified_at, kyc_approved_at, kyc_approved_by, kyc_rejected_at, kyc_rejected_by, kyc_rejection_reason, kyc_admin_notes, kyc_id_status, kyc_id_url, kyc_id_uploaded_at, kyc_id_notes, kyc_address_status, kyc_address_url, kyc_address_uploaded_at, kyc_address_notes, kyc_selfie_status, kyc_selfie_url, kyc_selfie_uploaded_at, kyc_selfie_notes, kyc_bank_status, kyc_bank_url, kyc_bank_uploaded_at, kyc_bank_notes, role, parent_id, level, tree_path, commission_rate, tenant_id, last_login_at, last_login_ip, created_at, updated_at, referral_code, referred_by_code, referred_by_user_id, has_purchased_program, first_purchase_at, total_purchases, total_referrals, active_referrals, referral_earnings, can_create_same_role) FROM stdin;
100	infT@marketedgepros.com	scrypt:32768:8:1$gKhiunz2tqQa9Du0$9a3c7bfe15eaf33ae52d92fdd3afe5bc5444823d0d0fed004ae30a3ce36bfb2c41a2b03ab6477f2638c4b07b89912e60c0e5a5bce5a0f25d90ba86d53c702051	גג	גגכ		+1	\N	\N	t	t	\N	f	\N	not_submitted	\N	\N	\N	\N	\N	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	super_admin	99	2	1.99.100	0.00	\N	2025-10-25 21:32:13.680868	127.0.0.1	2025-10-25 18:43:18.563526	2025-10-25 21:32:13.682156	VYZAC18W	\N	\N	f	\N	0	0	0	0.00	f
102	gabay037@gmail.com	scrypt:32768:8:1$EKhkmUl3T0A39KLF$142c375ac5ff3d335ad61e5831cc6c3754936047a81770c75502114296c68ffac975b9fb3ca982c7d72749dfa8363e55b63c37bfdeb781acaed219c342a9bdbc	liav	gabay	+972547891728	US	\N	\N	t	f	\N	f	\N	not_submitted	\N	\N	\N	\N	\N	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	trader	\N	0	\N	0.00	\N	2025-10-27 23:48:44.830282	127.0.0.1	2025-10-27 18:50:36.040697	2025-10-28 10:23:58.251292	\N	\N	\N	f	\N	0	0	0	0.00	f
97	newsupermaster@test.com	scrypt:32768:8:1$N0IGjMnFJRScr8lm$d8331ea6fd529a0a5dabd142c7290d77f90c2160f202e3760a0591541a988b35d207e0a2e58c6b6c676ea888f5d58dfd046b75daa76042e676fe65afd5106f82	New	Supermaster	\N	\N	\N	\N	t	t	\N	f	\N	not_submitted	\N	\N	\N	\N	\N	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	supermaster	77	1	1.97	0.00	\N	\N	\N	2025-10-25 18:16:35.774705	2025-10-25 18:16:35.797258	PXV67IOL	\N	\N	f	\N	0	0	0	0.00	f
98	newadmin2@test.com	scrypt:32768:8:1$9khe5AP0qIkKaCfU$29b86fffd4121c68011fce25069f75da552afd6ef2706766e2684928de27c038543dbd4cd84cb301e23dec95d0c35aaf248c2116a1b55e21ed3d42b341af3bca	New	Admin2	\N	\N	\N	\N	t	t	\N	f	\N	not_submitted	\N	\N	\N	\N	\N	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	admin	78	2	1.1.98	0.00	\N	\N	\N	2025-10-25 18:16:39.178727	2025-10-25 18:16:39.220461	JPD2ZAQQ	\N	\N	f	\N	0	0	0	0.00	f
86	newadmin@test.com	scrypt:32768:8:1$SqRZOrXDlD1HssjM$b16e8ce8696bc79e784cdc68b84d562696602b2faac20d1d1844689e7a8eebe6bdaec68c7fbae8d867f3dd2959f1ba3680c3075566ef59d2cfe5ddb61d02e0cd	New	Admin	\N	\N	\N	\N	t	t	\N	f	\N	not_submitted	\N	\N	\N	\N	\N	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	admin	78	2	1.1.86	0.00	\N	2025-10-27 22:15:59.574005	127.0.0.1	2025-10-25 17:40:01.953489	2025-10-27 22:15:59.577537	\N	\N	\N	f	\N	0	0	0	0.00	f
78	info@marketedgepros.com	scrypt:32768:8:1$cPxKMcgBF0EKSeyE$4f1c27b5c77394915f9869bae27e116169353c451d025531cc9a9736a45a5946976035f093c138be3753dbd7bdfc98afaf0c77840d5f167160bd384bbf671d17	Info	Admin	\N	\N	\N	\N	t	t	\N	f	\N	not_submitted	\N	\N	\N	\N	\N	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	supermaster	77	1	1.1	0.00	\N	2025-10-30 18:12:15.947656	127.0.0.1	2025-10-25 17:19:20.811125	2025-10-30 18:12:15.952037	\N	\N	\N	f	\N	0	0	0	0.00	f
77	supermaster@marketedgepros.com	scrypt:32768:8:1$PvezjZxwZLYHKlcl$1fe495fa413c27476069c535ada85ee311510f188e7b3f85fdd5a0f05fff24c8e1cf828934b6f14a5cfe040e15eafa9f50a29d085717ac36a1cb599ee66ddf2a	Super	Master	\N	\N	\N	\N	t	t	\N	f	\N	not_submitted	\N	\N	\N	\N	\N	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	supermaster	\N	0	1	0.00	\N	2025-10-30 19:50:00.799444	127.0.0.1	2025-10-25 17:19:20.657248	2025-10-30 19:50:00.800614	\N	\N	\N	f	\N	0	0	0	0.00	t
99	infP@marketedgepros.com	scrypt:32768:8:1$LQAihwTpmTVloKt6$9d8a62c282c985b1e65292212328041cec49be9e6d5277388b55b329352d8fd26b06dc7ddc14a907618c8be693370e6e31b940f183363ff14c86a1dcd4316e4b	גגג	כככ		+1	\N	\N	t	t	\N	f	\N	not_submitted	\N	\N	\N	\N	\N	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	supermaster	77	1	1.99	0.00	\N	2025-10-25 18:43:31.56534	127.0.0.1	2025-10-25 18:19:18.645099	2025-10-25 18:43:31.566312	OHBNZW57	\N	\N	f	\N	0	0	0	0.00	f
101	affiliate@test.com	scrypt:32768:8:1$DgacxZ6FjD1sjWvX$7180780da15026542b28a346cd762ba5f90717a07ed1e53c51eef3321d88a90908a1c948a2a881d8bb942204cf5d1bd104bb289c2f4ff3f32b5cc55c50952ec7	Affiliate	Test	1234567890	+1	\N	\N	t	t	\N	f	\N	not_submitted	\N	\N	\N	\N	\N	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	master	78	2	1.1.101	0.00	\N	2025-10-26 20:09:47.328692	127.0.0.1	2025-10-26 20:08:57.117127	2025-10-26 20:09:47.331202	\N	\N	\N	f	\N	0	0	0	0.00	f
79	agent@marketedgepros.com	scrypt:32768:8:1$uyxqJ95ZSFXG7StL$84e3a7b80e09320d94cc3538e97d3de21529e77d2d068270ba16691847f355cf96df5934687c042aba72a746a27ff2abf889bee5ffe38d62fd0341e7563c8e28	Test	Agent	\N	\N	\N	\N	t	t	\N	f	\N	not_submitted	\N	\N	\N	\N	\N	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	affiliate	78	2	1.1.1	0.00	\N	2025-10-29 00:35:33.505488	127.0.0.1	2025-10-25 17:19:21.105292	2025-10-29 00:35:33.506628	\N	\N	\N	f	\N	0	0	0	0.00	f
103	spendmoneysmart1@gmail.com	scrypt:32768:8:1$QutUayP7fd2YnrSE$123efa4f6c1e0bb52834dc994a8844202a66368ca59a1e4c85e05f3787aca73a26f4af91055dfc19f9d0114d9d36397e29f6ed19324343c515c26ce5af3ca501	Andrew	Firlit		US	\N	\N	f	t	2025-10-29 07:27:42.666616	f	\N	not_submitted	\N	\N	\N	\N	\N	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	guest	\N	0	\N	0.00	\N	2025-10-29 07:27:49.821223	127.0.0.1	2025-10-29 07:26:39.625529	2025-10-30 11:39:41.279695	\N	\N	\N	f	\N	0	0	0	0.00	f
87	newtrader@test.com	scrypt:32768:8:1$Q8F2f611qEtatks0$76130e59a44a35c1725b7c7f1a83b64061966113bef3697d2d5cac6b4884c39be076ad4a611b1c0409cfa7e7b4d6a29396af9da3520c601aeddd8abc2538b98c	New	Trader	\N	\N	\N	/uploads/profiles/87/avatar.png	t	t	\N	f	\N	not_submitted	\N	\N	\N	\N	\N	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	trader	79	3	1.1.1.87	0.00	\N	2025-10-29 00:48:32.881425	127.0.0.1	2025-10-25 17:40:03.673527	2025-10-29 00:48:32.883618	\N	\N	\N	f	\N	0	0	0	0.00	f
85	newsuper@test.com	scrypt:32768:8:1$gGrQA2u1fbwVQ6BT$dec2cd81be2ac04a2da244ebfc2cc14cf5851d6ac035f81d040710878d809a3ed8b4bc081a4be2d98657601a6ca432af4990790a4eacb3de3450bd9d4d5c2c02	New	SuperAdmin	\N	\N	\N	\N	t	t	\N	f	\N	not_submitted	\N	\N	\N	\N	\N	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	super_admin	77	1	1.85	0.00	\N	\N	\N	2025-10-25 17:40:00.247308	2025-10-25 17:40:00.26462	\N	\N	\N	f	\N	0	0	0	0.00	f
80	supermaster2@marketedgepros.com	scrypt:32768:8:1$3mHeZSFDwHV3J0Uq$e44702cff6870e3b686873cb223ed6805d618b3d572c84320197396e8c096cc33553ef0aab4563f6de173302cf3f7fd67bf8716d2c7377ef740223770d77425f	Super	Master 2	\N	\N	\N	\N	f	t	\N	f	\N	not_submitted	\N	\N	\N	\N	\N	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	not_uploaded	\N	\N	\N	supermaster	\N	0	2	0.00	\N	\N	\N	2025-10-25 17:19:21.105302	2025-10-25 17:48:57.099781	\N	\N	\N	f	\N	0	0	0	0.00	t
\.


--
-- Data for Name: verification_attempts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.verification_attempts (id, email, code_entered, success, ip_address, user_agent, failure_reason, created_at, updated_at) FROM stdin;
8	spendmoneysmart1@gmail.com	578598	t	127.0.0.1	Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36	\N	2025-10-29 07:27:42.674152	2025-10-29 07:27:42.674158
\.


--
-- Data for Name: wallets; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.wallets (id, user_id, main_balance, commission_balance, bonus_balance, last_transaction_at, is_active, notes, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: withdrawals; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.withdrawals (id, agent_id, amount, fee, net_amount, payment_method, payment_details, status, approved_by, approved_at, processed_at, completed_at, transaction_id, rejection_reason, notes, created_at, updated_at) FROM stdin;
\.


--
-- Name: affiliate_commissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.affiliate_commissions_id_seq', 1, false);


--
-- Name: affiliate_links_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.affiliate_links_id_seq', 1, false);


--
-- Name: affiliate_payouts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.affiliate_payouts_id_seq', 1, false);


--
-- Name: affiliate_referrals_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.affiliate_referrals_id_seq', 1, false);


--
-- Name: affiliate_settings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.affiliate_settings_id_seq', 3, true);


--
-- Name: agents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.agents_id_seq', 1, false);


--
-- Name: blog_posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.blog_posts_id_seq', 14, true);


--
-- Name: challenges_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.challenges_id_seq', 23, true);


--
-- Name: commission_balances_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.commission_balances_id_seq', 1, false);


--
-- Name: commission_rules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.commission_rules_id_seq', 6, true);


--
-- Name: commission_withdrawals_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.commission_withdrawals_id_seq', 1, false);


--
-- Name: commissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.commissions_id_seq', 1, false);


--
-- Name: course_enrollments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.course_enrollments_id_seq', 4, true);


--
-- Name: email_queue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.email_queue_id_seq', 1, true);


--
-- Name: email_verification_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.email_verification_tokens_id_seq', 13, true);


--
-- Name: faqs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.faqs_id_seq', 10, true);


--
-- Name: lead_activities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.lead_activities_id_seq', 1, false);


--
-- Name: lead_notes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.lead_notes_id_seq', 1, false);


--
-- Name: leads_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.leads_id_seq', 4, true);


--
-- Name: notification_preferences_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.notification_preferences_id_seq', 1, true);


--
-- Name: notifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.notifications_id_seq', 1, false);


--
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.password_reset_tokens_id_seq', 1, true);


--
-- Name: payment_approval_requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.payment_approval_requests_id_seq', 1, false);


--
-- Name: payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.payments_id_seq', 9, true);


--
-- Name: program_addons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.program_addons_id_seq', 32, true);


--
-- Name: referrals_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.referrals_id_seq', 1, false);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.roles_id_seq', 5, true);


--
-- Name: support_articles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.support_articles_id_seq', 1, false);


--
-- Name: support_tickets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.support_tickets_id_seq', 1, false);


--
-- Name: tenants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tenants_id_seq', 7, true);


--
-- Name: ticket_messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ticket_messages_id_seq', 1, false);


--
-- Name: trades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.trades_id_seq', 1, false);


--
-- Name: trading_programs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.trading_programs_id_seq', 37, true);


--
-- Name: transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.transactions_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 103, true);


--
-- Name: verification_attempts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.verification_attempts_id_seq', 8, true);


--
-- Name: wallets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.wallets_id_seq', 1, false);


--
-- Name: withdrawals_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.withdrawals_id_seq', 1, false);


--
-- Name: affiliate_commissions affiliate_commissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_commissions
    ADD CONSTRAINT affiliate_commissions_pkey PRIMARY KEY (id);


--
-- Name: affiliate_links affiliate_links_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_links
    ADD CONSTRAINT affiliate_links_code_key UNIQUE (code);


--
-- Name: affiliate_links affiliate_links_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_links
    ADD CONSTRAINT affiliate_links_pkey PRIMARY KEY (id);


--
-- Name: affiliate_payouts affiliate_payouts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_payouts
    ADD CONSTRAINT affiliate_payouts_pkey PRIMARY KEY (id);


--
-- Name: affiliate_referrals affiliate_referrals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_referrals
    ADD CONSTRAINT affiliate_referrals_pkey PRIMARY KEY (id);


--
-- Name: affiliate_settings affiliate_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_settings
    ADD CONSTRAINT affiliate_settings_pkey PRIMARY KEY (id);


--
-- Name: agents agents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agents
    ADD CONSTRAINT agents_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: blog_posts blog_posts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_posts
    ADD CONSTRAINT blog_posts_pkey PRIMARY KEY (id);


--
-- Name: blog_posts blog_posts_slug_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_posts
    ADD CONSTRAINT blog_posts_slug_key UNIQUE (slug);


--
-- Name: challenges challenges_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.challenges
    ADD CONSTRAINT challenges_pkey PRIMARY KEY (id);


--
-- Name: commission_balances commission_balances_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_balances
    ADD CONSTRAINT commission_balances_pkey PRIMARY KEY (id);


--
-- Name: commission_balances commission_balances_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_balances
    ADD CONSTRAINT commission_balances_user_id_key UNIQUE (user_id);


--
-- Name: commission_rules commission_rules_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_rules
    ADD CONSTRAINT commission_rules_pkey PRIMARY KEY (id);


--
-- Name: commission_withdrawals commission_withdrawals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_withdrawals
    ADD CONSTRAINT commission_withdrawals_pkey PRIMARY KEY (id);


--
-- Name: commissions commissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commissions
    ADD CONSTRAINT commissions_pkey PRIMARY KEY (id);


--
-- Name: course_enrollments course_enrollments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course_enrollments
    ADD CONSTRAINT course_enrollments_pkey PRIMARY KEY (id);


--
-- Name: email_queue email_queue_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_queue
    ADD CONSTRAINT email_queue_pkey PRIMARY KEY (id);


--
-- Name: email_verification_tokens email_verification_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_verification_tokens
    ADD CONSTRAINT email_verification_tokens_pkey PRIMARY KEY (id);


--
-- Name: faqs faqs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.faqs
    ADD CONSTRAINT faqs_pkey PRIMARY KEY (id);


--
-- Name: lead_activities lead_activities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lead_activities
    ADD CONSTRAINT lead_activities_pkey PRIMARY KEY (id);


--
-- Name: lead_notes lead_notes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lead_notes
    ADD CONSTRAINT lead_notes_pkey PRIMARY KEY (id);


--
-- Name: leads leads_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.leads
    ADD CONSTRAINT leads_pkey PRIMARY KEY (id);


--
-- Name: notification_preferences notification_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_preferences
    ADD CONSTRAINT notification_preferences_pkey PRIMARY KEY (id);


--
-- Name: notification_preferences notification_preferences_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_preferences
    ADD CONSTRAINT notification_preferences_user_id_key UNIQUE (user_id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: password_reset_tokens password_reset_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_pkey PRIMARY KEY (id);


--
-- Name: payment_approval_requests payment_approval_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment_approval_requests
    ADD CONSTRAINT payment_approval_requests_pkey PRIMARY KEY (id);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- Name: payments payments_transaction_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_transaction_id_key UNIQUE (transaction_id);


--
-- Name: program_addons program_addons_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.program_addons
    ADD CONSTRAINT program_addons_pkey PRIMARY KEY (id);


--
-- Name: referrals referrals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT referrals_pkey PRIMARY KEY (id);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: support_articles support_articles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_articles
    ADD CONSTRAINT support_articles_pkey PRIMARY KEY (id);


--
-- Name: support_articles support_articles_slug_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_articles
    ADD CONSTRAINT support_articles_slug_key UNIQUE (slug);


--
-- Name: support_tickets support_tickets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_tickets
    ADD CONSTRAINT support_tickets_pkey PRIMARY KEY (id);


--
-- Name: support_tickets support_tickets_ticket_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_tickets
    ADD CONSTRAINT support_tickets_ticket_number_key UNIQUE (ticket_number);


--
-- Name: tenants tenants_custom_domain_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tenants
    ADD CONSTRAINT tenants_custom_domain_key UNIQUE (custom_domain);


--
-- Name: tenants tenants_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tenants
    ADD CONSTRAINT tenants_pkey PRIMARY KEY (id);


--
-- Name: ticket_messages ticket_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ticket_messages
    ADD CONSTRAINT ticket_messages_pkey PRIMARY KEY (id);


--
-- Name: trades trades_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trades
    ADD CONSTRAINT trades_pkey PRIMARY KEY (id);


--
-- Name: trades trades_ticket_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trades
    ADD CONSTRAINT trades_ticket_key UNIQUE (ticket);


--
-- Name: trading_programs trading_programs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trading_programs
    ADD CONSTRAINT trading_programs_pkey PRIMARY KEY (id);


--
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);


--
-- Name: course_enrollments unique_course_email; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.course_enrollments
    ADD CONSTRAINT unique_course_email UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_referral_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_referral_code_key UNIQUE (referral_code);


--
-- Name: verification_attempts verification_attempts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.verification_attempts
    ADD CONSTRAINT verification_attempts_pkey PRIMARY KEY (id);


--
-- Name: wallets wallets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wallets
    ADD CONSTRAINT wallets_pkey PRIMARY KEY (id);


--
-- Name: wallets wallets_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wallets
    ADD CONSTRAINT wallets_user_id_key UNIQUE (user_id);


--
-- Name: withdrawals withdrawals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.withdrawals
    ADD CONSTRAINT withdrawals_pkey PRIMARY KEY (id);


--
-- Name: idx_affiliate_commissions_affiliate_user; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_affiliate_commissions_affiliate_user ON public.affiliate_commissions USING btree (affiliate_user_id);


--
-- Name: idx_affiliate_commissions_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_affiliate_commissions_status ON public.affiliate_commissions USING btree (status);


--
-- Name: idx_affiliate_links_code; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_affiliate_links_code ON public.affiliate_links USING btree (code);


--
-- Name: idx_affiliate_links_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_affiliate_links_user_id ON public.affiliate_links USING btree (user_id);


--
-- Name: idx_affiliate_payouts_affiliate_user; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_affiliate_payouts_affiliate_user ON public.affiliate_payouts USING btree (affiliate_user_id);


--
-- Name: idx_affiliate_payouts_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_affiliate_payouts_status ON public.affiliate_payouts USING btree (status);


--
-- Name: idx_affiliate_referrals_affiliate_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_affiliate_referrals_affiliate_link ON public.affiliate_referrals USING btree (affiliate_link_id);


--
-- Name: idx_affiliate_referrals_affiliate_user; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_affiliate_referrals_affiliate_user ON public.affiliate_referrals USING btree (affiliate_user_id);


--
-- Name: idx_affiliate_referrals_referred_user; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_affiliate_referrals_referred_user ON public.affiliate_referrals USING btree (referred_user_id);


--
-- Name: idx_affiliate_referrals_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_affiliate_referrals_status ON public.affiliate_referrals USING btree (status);


--
-- Name: idx_approval_requests_challenge_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_approval_requests_challenge_id ON public.payment_approval_requests USING btree (challenge_id);


--
-- Name: idx_approval_requests_requested_by; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_approval_requests_requested_by ON public.payment_approval_requests USING btree (requested_by);


--
-- Name: idx_approval_requests_requested_for; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_approval_requests_requested_for ON public.payment_approval_requests USING btree (requested_for);


--
-- Name: idx_approval_requests_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_approval_requests_status ON public.payment_approval_requests USING btree (status);


--
-- Name: idx_blog_category_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_blog_category_status ON public.blog_posts USING btree (category, status);


--
-- Name: idx_blog_featured_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_blog_featured_status ON public.blog_posts USING btree (featured, status);


--
-- Name: idx_blog_posts_author_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_blog_posts_author_id ON public.blog_posts USING btree (author_id);


--
-- Name: idx_blog_posts_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_blog_posts_category ON public.blog_posts USING btree (category);


--
-- Name: idx_blog_posts_featured; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_blog_posts_featured ON public.blog_posts USING btree (featured);


--
-- Name: idx_blog_posts_published_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_blog_posts_published_at ON public.blog_posts USING btree (published_at);


--
-- Name: idx_blog_posts_search; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_blog_posts_search ON public.blog_posts USING gin (to_tsvector('english'::regconfig, (((((title)::text || ' '::text) || COALESCE(excerpt, ''::text)) || ' '::text) || COALESCE(content, ''::text))));


--
-- Name: idx_blog_posts_slug; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_blog_posts_slug ON public.blog_posts USING btree (slug);


--
-- Name: idx_blog_posts_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_blog_posts_status ON public.blog_posts USING btree (status);


--
-- Name: idx_blog_status_published; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_blog_status_published ON public.blog_posts USING btree (status, published_at);


--
-- Name: idx_challenges_approval_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_challenges_approval_status ON public.challenges USING btree (approval_status);


--
-- Name: idx_challenges_created_by; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_challenges_created_by ON public.challenges USING btree (created_by);


--
-- Name: idx_challenges_payment_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_challenges_payment_type ON public.challenges USING btree (payment_type);


--
-- Name: idx_commission_balances_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_commission_balances_user_id ON public.commission_balances USING btree (user_id);


--
-- Name: idx_commission_rules_active; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_commission_rules_active ON public.commission_rules USING btree (is_active);


--
-- Name: idx_commission_rules_role; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_commission_rules_role ON public.commission_rules USING btree (target_role);


--
-- Name: idx_commission_rules_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_commission_rules_type ON public.commission_rules USING btree (rule_type);


--
-- Name: idx_commission_withdrawals_requested_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_commission_withdrawals_requested_at ON public.commission_withdrawals USING btree (requested_at);


--
-- Name: idx_commission_withdrawals_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_commission_withdrawals_status ON public.commission_withdrawals USING btree (status);


--
-- Name: idx_commission_withdrawals_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_commission_withdrawals_user_id ON public.commission_withdrawals USING btree (user_id);


--
-- Name: idx_commissions_level; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_commissions_level ON public.commissions USING btree (level);


--
-- Name: idx_commissions_source_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_commissions_source_id ON public.commissions USING btree (source_id);


--
-- Name: idx_commissions_source_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_commissions_source_type ON public.commissions USING btree (source_type);


--
-- Name: idx_commissions_source_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_commissions_source_user_id ON public.commissions USING btree (source_user_id);


--
-- Name: idx_commissions_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_commissions_status ON public.commissions USING btree (status);


--
-- Name: idx_commissions_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_commissions_user_id ON public.commissions USING btree (user_id);


--
-- Name: idx_course_enrollments_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_course_enrollments_email ON public.course_enrollments USING btree (email);


--
-- Name: idx_course_enrollments_enrolled_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_course_enrollments_enrolled_at ON public.course_enrollments USING btree (enrolled_at);


--
-- Name: idx_course_enrollments_unsubscribed; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_course_enrollments_unsubscribed ON public.course_enrollments USING btree (unsubscribed);


--
-- Name: idx_email_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_email_created ON public.verification_attempts USING btree (email, created_at);


--
-- Name: idx_email_queue_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_email_queue_created_at ON public.email_queue USING btree (created_at);


--
-- Name: idx_email_queue_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_email_queue_status ON public.email_queue USING btree (status);


--
-- Name: idx_faqs_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_faqs_category ON public.faqs USING btree (category);


--
-- Name: idx_faqs_category_order; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_faqs_category_order ON public.faqs USING btree (category, "order");


--
-- Name: idx_faqs_is_featured; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_faqs_is_featured ON public.faqs USING btree (is_featured);


--
-- Name: idx_faqs_is_published; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_faqs_is_published ON public.faqs USING btree (is_published);


--
-- Name: idx_faqs_order; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_faqs_order ON public.faqs USING btree ("order");


--
-- Name: idx_ip_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ip_created ON public.verification_attempts USING btree (ip_address, created_at);


--
-- Name: idx_notifications_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_notifications_created_at ON public.notifications USING btree (created_at);


--
-- Name: idx_notifications_is_read; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_notifications_is_read ON public.notifications USING btree (is_read);


--
-- Name: idx_notifications_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_notifications_type ON public.notifications USING btree (type);


--
-- Name: idx_notifications_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_notifications_user_id ON public.notifications USING btree (user_id);


--
-- Name: idx_payments_approval_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_payments_approval_status ON public.payments USING btree (approval_status);


--
-- Name: idx_payments_payment_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_payments_payment_type ON public.payments USING btree (payment_type);


--
-- Name: idx_success_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_success_created ON public.verification_attempts USING btree (success, created_at);


--
-- Name: idx_support_articles_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_support_articles_category ON public.support_articles USING btree (category);


--
-- Name: idx_support_articles_featured; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_support_articles_featured ON public.support_articles USING btree (featured);


--
-- Name: idx_support_articles_published_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_support_articles_published_at ON public.support_articles USING btree (published_at);


--
-- Name: idx_support_articles_search; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_support_articles_search ON public.support_articles USING gin (to_tsvector('english'::regconfig, (((title)::text || ' '::text) || content)));


--
-- Name: idx_support_articles_slug; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_support_articles_slug ON public.support_articles USING btree (slug);


--
-- Name: idx_support_articles_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_support_articles_status ON public.support_articles USING btree (status);


--
-- Name: idx_support_tickets_assigned_to; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_support_tickets_assigned_to ON public.support_tickets USING btree (assigned_to);


--
-- Name: idx_support_tickets_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_support_tickets_category ON public.support_tickets USING btree (category);


--
-- Name: idx_support_tickets_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_support_tickets_created_at ON public.support_tickets USING btree (created_at DESC);


--
-- Name: idx_support_tickets_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_support_tickets_email ON public.support_tickets USING btree (email);


--
-- Name: idx_support_tickets_priority; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_support_tickets_priority ON public.support_tickets USING btree (priority);


--
-- Name: idx_support_tickets_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_support_tickets_status ON public.support_tickets USING btree (status);


--
-- Name: idx_support_tickets_status_priority; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_support_tickets_status_priority ON public.support_tickets USING btree (status, priority);


--
-- Name: idx_support_tickets_ticket_number; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_support_tickets_ticket_number ON public.support_tickets USING btree (ticket_number);


--
-- Name: idx_support_tickets_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_support_tickets_user_id ON public.support_tickets USING btree (user_id);


--
-- Name: idx_ticket_messages_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ticket_messages_created_at ON public.ticket_messages USING btree (created_at DESC);


--
-- Name: idx_ticket_messages_is_staff; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ticket_messages_is_staff ON public.ticket_messages USING btree (is_staff);


--
-- Name: idx_ticket_messages_ticket_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ticket_messages_ticket_id ON public.ticket_messages USING btree (ticket_id);


--
-- Name: idx_ticket_messages_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ticket_messages_user_id ON public.ticket_messages USING btree (user_id);


--
-- Name: idx_users_referral_code; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_users_referral_code ON public.users USING btree (referral_code);


--
-- Name: idx_users_referred_by_code; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_users_referred_by_code ON public.users USING btree (referred_by_code);


--
-- Name: idx_users_referred_by_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_users_referred_by_user_id ON public.users USING btree (referred_by_user_id);


--
-- Name: ix_agents_agent_code; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_agents_agent_code ON public.agents USING btree (agent_code);


--
-- Name: ix_challenge_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_challenge_created_at ON public.challenges USING btree (created_at);


--
-- Name: ix_challenge_program_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_challenge_program_id ON public.challenges USING btree (program_id);


--
-- Name: ix_challenge_user_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_challenge_user_status ON public.challenges USING btree (user_id, status);


--
-- Name: ix_commission_agent_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_commission_agent_status ON public.commissions USING btree (agent_id, status);


--
-- Name: ix_commission_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_commission_created_at ON public.commissions USING btree (created_at);


--
-- Name: ix_email_verification_tokens_code; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_email_verification_tokens_code ON public.email_verification_tokens USING btree (code);


--
-- Name: ix_email_verification_tokens_token; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_email_verification_tokens_token ON public.email_verification_tokens USING btree (token);


--
-- Name: ix_lead_activities_activity_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_lead_activities_activity_type ON public.lead_activities USING btree (activity_type);


--
-- Name: ix_lead_activities_lead_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_lead_activities_lead_id ON public.lead_activities USING btree (lead_id);


--
-- Name: ix_lead_notes_lead_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_lead_notes_lead_id ON public.lead_notes USING btree (lead_id);


--
-- Name: ix_leads_assigned_to; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_leads_assigned_to ON public.leads USING btree (assigned_to);


--
-- Name: ix_leads_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_leads_email ON public.leads USING btree (email);


--
-- Name: ix_leads_next_follow_up; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_leads_next_follow_up ON public.leads USING btree (next_follow_up);


--
-- Name: ix_leads_source; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_leads_source ON public.leads USING btree (source);


--
-- Name: ix_leads_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_leads_status ON public.leads USING btree (status);


--
-- Name: ix_password_reset_tokens_code; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_password_reset_tokens_code ON public.password_reset_tokens USING btree (code);


--
-- Name: ix_password_reset_tokens_token; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_password_reset_tokens_token ON public.password_reset_tokens USING btree (token);


--
-- Name: ix_referral_agent_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_referral_agent_id ON public.referrals USING btree (agent_id);


--
-- Name: ix_referral_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_referral_status ON public.referrals USING btree (status);


--
-- Name: ix_referrals_referral_code; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_referrals_referral_code ON public.referrals USING btree (referral_code);


--
-- Name: ix_tenants_subdomain; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_tenants_subdomain ON public.tenants USING btree (subdomain);


--
-- Name: ix_transaction_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_transaction_created_at ON public.transactions USING btree (created_at);


--
-- Name: ix_transaction_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_transaction_type ON public.transactions USING btree (type);


--
-- Name: ix_transaction_wallet_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_transaction_wallet_id ON public.transactions USING btree (wallet_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_level; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_level ON public.users USING btree (level);


--
-- Name: ix_users_parent_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_parent_id ON public.users USING btree (parent_id);


--
-- Name: ix_users_tree_path; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_users_tree_path ON public.users USING btree (tree_path);


--
-- Name: ix_verification_attempts_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_verification_attempts_email ON public.verification_attempts USING btree (email);


--
-- Name: ix_wallet_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_wallet_user_id ON public.wallets USING btree (user_id);


--
-- Name: blog_posts trigger_update_blog_posts_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_update_blog_posts_updated_at BEFORE UPDATE ON public.blog_posts FOR EACH ROW EXECUTE FUNCTION public.update_blog_posts_updated_at();


--
-- Name: faqs trigger_update_faqs_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_update_faqs_updated_at BEFORE UPDATE ON public.faqs FOR EACH ROW EXECUTE FUNCTION public.update_faqs_updated_at();


--
-- Name: payment_approval_requests trigger_update_payment_approval_requests_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_update_payment_approval_requests_updated_at BEFORE UPDATE ON public.payment_approval_requests FOR EACH ROW EXECUTE FUNCTION public.update_payment_approval_requests_updated_at();


--
-- Name: support_tickets trigger_update_support_tickets_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trigger_update_support_tickets_updated_at BEFORE UPDATE ON public.support_tickets FOR EACH ROW EXECUTE FUNCTION public.update_support_tickets_updated_at();


--
-- Name: affiliate_commissions affiliate_commissions_affiliate_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_commissions
    ADD CONSTRAINT affiliate_commissions_affiliate_user_id_fkey FOREIGN KEY (affiliate_user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: affiliate_commissions affiliate_commissions_payout_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_commissions
    ADD CONSTRAINT affiliate_commissions_payout_id_fkey FOREIGN KEY (payout_id) REFERENCES public.affiliate_payouts(id) ON DELETE SET NULL;


--
-- Name: affiliate_commissions affiliate_commissions_referral_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_commissions
    ADD CONSTRAINT affiliate_commissions_referral_id_fkey FOREIGN KEY (referral_id) REFERENCES public.affiliate_referrals(id) ON DELETE SET NULL;


--
-- Name: affiliate_links affiliate_links_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_links
    ADD CONSTRAINT affiliate_links_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: affiliate_payouts affiliate_payouts_affiliate_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_payouts
    ADD CONSTRAINT affiliate_payouts_affiliate_user_id_fkey FOREIGN KEY (affiliate_user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: affiliate_referrals affiliate_referrals_affiliate_link_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_referrals
    ADD CONSTRAINT affiliate_referrals_affiliate_link_id_fkey FOREIGN KEY (affiliate_link_id) REFERENCES public.affiliate_links(id) ON DELETE CASCADE;


--
-- Name: affiliate_referrals affiliate_referrals_affiliate_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_referrals
    ADD CONSTRAINT affiliate_referrals_affiliate_user_id_fkey FOREIGN KEY (affiliate_user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: affiliate_referrals affiliate_referrals_program_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_referrals
    ADD CONSTRAINT affiliate_referrals_program_id_fkey FOREIGN KEY (program_id) REFERENCES public.trading_programs(id) ON DELETE SET NULL;


--
-- Name: affiliate_referrals affiliate_referrals_referred_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_referrals
    ADD CONSTRAINT affiliate_referrals_referred_user_id_fkey FOREIGN KEY (referred_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: agents agents_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.agents
    ADD CONSTRAINT agents_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: blog_posts blog_posts_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.blog_posts
    ADD CONSTRAINT blog_posts_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: challenges challenges_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.challenges
    ADD CONSTRAINT challenges_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);


--
-- Name: challenges challenges_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.challenges
    ADD CONSTRAINT challenges_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: challenges challenges_program_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.challenges
    ADD CONSTRAINT challenges_program_id_fkey FOREIGN KEY (program_id) REFERENCES public.trading_programs(id);


--
-- Name: challenges challenges_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.challenges
    ADD CONSTRAINT challenges_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: commission_balances commission_balances_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_balances
    ADD CONSTRAINT commission_balances_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: commission_withdrawals commission_withdrawals_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_withdrawals
    ADD CONSTRAINT commission_withdrawals_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);


--
-- Name: commission_withdrawals commission_withdrawals_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_withdrawals
    ADD CONSTRAINT commission_withdrawals_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: commissions commissions_agent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commissions
    ADD CONSTRAINT commissions_agent_id_fkey FOREIGN KEY (agent_id) REFERENCES public.agents(id);


--
-- Name: commissions commissions_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commissions
    ADD CONSTRAINT commissions_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);


--
-- Name: commissions commissions_challenge_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commissions
    ADD CONSTRAINT commissions_challenge_id_fkey FOREIGN KEY (challenge_id) REFERENCES public.challenges(id);


--
-- Name: commissions commissions_referral_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commissions
    ADD CONSTRAINT commissions_referral_id_fkey FOREIGN KEY (referral_id) REFERENCES public.referrals(id);


--
-- Name: commissions commissions_rule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commissions
    ADD CONSTRAINT commissions_rule_id_fkey FOREIGN KEY (rule_id) REFERENCES public.commission_rules(id);


--
-- Name: commissions commissions_source_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commissions
    ADD CONSTRAINT commissions_source_user_id_fkey FOREIGN KEY (source_user_id) REFERENCES public.users(id);


--
-- Name: commissions commissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commissions
    ADD CONSTRAINT commissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: email_queue email_queue_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_queue
    ADD CONSTRAINT email_queue_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: email_verification_tokens email_verification_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_verification_tokens
    ADD CONSTRAINT email_verification_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: affiliate_commissions fk_commission_payout; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.affiliate_commissions
    ADD CONSTRAINT fk_commission_payout FOREIGN KEY (payout_id) REFERENCES public.affiliate_payouts(id) ON DELETE SET NULL;


--
-- Name: lead_activities lead_activities_lead_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lead_activities
    ADD CONSTRAINT lead_activities_lead_id_fkey FOREIGN KEY (lead_id) REFERENCES public.leads(id);


--
-- Name: lead_activities lead_activities_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lead_activities
    ADD CONSTRAINT lead_activities_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: lead_notes lead_notes_lead_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lead_notes
    ADD CONSTRAINT lead_notes_lead_id_fkey FOREIGN KEY (lead_id) REFERENCES public.leads(id);


--
-- Name: lead_notes lead_notes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lead_notes
    ADD CONSTRAINT lead_notes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: leads leads_assigned_to_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.leads
    ADD CONSTRAINT leads_assigned_to_fkey FOREIGN KEY (assigned_to) REFERENCES public.users(id);


--
-- Name: leads leads_converted_to_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.leads
    ADD CONSTRAINT leads_converted_to_user_id_fkey FOREIGN KEY (converted_to_user_id) REFERENCES public.users(id);


--
-- Name: notification_preferences notification_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_preferences
    ADD CONSTRAINT notification_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: password_reset_tokens password_reset_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: payment_approval_requests payment_approval_requests_challenge_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment_approval_requests
    ADD CONSTRAINT payment_approval_requests_challenge_id_fkey FOREIGN KEY (challenge_id) REFERENCES public.challenges(id) ON DELETE CASCADE;


--
-- Name: payment_approval_requests payment_approval_requests_payment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment_approval_requests
    ADD CONSTRAINT payment_approval_requests_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payments(id) ON DELETE CASCADE;


--
-- Name: payment_approval_requests payment_approval_requests_requested_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment_approval_requests
    ADD CONSTRAINT payment_approval_requests_requested_by_fkey FOREIGN KEY (requested_by) REFERENCES public.users(id);


--
-- Name: payment_approval_requests payment_approval_requests_requested_for_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment_approval_requests
    ADD CONSTRAINT payment_approval_requests_requested_for_fkey FOREIGN KEY (requested_for) REFERENCES public.users(id);


--
-- Name: payment_approval_requests payment_approval_requests_reviewed_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment_approval_requests
    ADD CONSTRAINT payment_approval_requests_reviewed_by_fkey FOREIGN KEY (reviewed_by) REFERENCES public.users(id);


--
-- Name: payments payments_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);


--
-- Name: payments payments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: program_addons program_addons_program_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.program_addons
    ADD CONSTRAINT program_addons_program_id_fkey FOREIGN KEY (program_id) REFERENCES public.trading_programs(id);


--
-- Name: referrals referrals_agent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT referrals_agent_id_fkey FOREIGN KEY (agent_id) REFERENCES public.agents(id);


--
-- Name: referrals referrals_referred_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT referrals_referred_user_id_fkey FOREIGN KEY (referred_user_id) REFERENCES public.users(id);


--
-- Name: support_articles support_articles_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_articles
    ADD CONSTRAINT support_articles_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- Name: support_tickets support_tickets_assigned_to_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_tickets
    ADD CONSTRAINT support_tickets_assigned_to_fkey FOREIGN KEY (assigned_to) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: support_tickets support_tickets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_tickets
    ADD CONSTRAINT support_tickets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: tenants tenants_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tenants
    ADD CONSTRAINT tenants_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.tenants(id);


--
-- Name: ticket_messages ticket_messages_ticket_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ticket_messages
    ADD CONSTRAINT ticket_messages_ticket_id_fkey FOREIGN KEY (ticket_id) REFERENCES public.support_tickets(id) ON DELETE CASCADE;


--
-- Name: ticket_messages ticket_messages_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ticket_messages
    ADD CONSTRAINT ticket_messages_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: trades trades_challenge_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trades
    ADD CONSTRAINT trades_challenge_id_fkey FOREIGN KEY (challenge_id) REFERENCES public.challenges(id);


--
-- Name: trading_programs trading_programs_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trading_programs
    ADD CONSTRAINT trading_programs_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenants(id);


--
-- Name: transactions transactions_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: transactions transactions_wallet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_wallet_id_fkey FOREIGN KEY (wallet_id) REFERENCES public.wallets(id);


--
-- Name: users users_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.users(id);


--
-- Name: users users_referred_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_referred_by_user_id_fkey FOREIGN KEY (referred_by_user_id) REFERENCES public.users(id);


--
-- Name: users users_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenants(id);


--
-- Name: wallets wallets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wallets
    ADD CONSTRAINT wallets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: withdrawals withdrawals_agent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.withdrawals
    ADD CONSTRAINT withdrawals_agent_id_fkey FOREIGN KEY (agent_id) REFERENCES public.agents(id);


--
-- Name: withdrawals withdrawals_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.withdrawals
    ADD CONSTRAINT withdrawals_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict c6PrtGfLBRZmnbnN1sVrUogEsPc9chGWr2Uf6Lw9eykac1vYbcZpciArV3AgOqf

