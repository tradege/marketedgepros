--
-- PostgreSQL database dump
--

\restrict PfqoKhBweiGF2u8biCMcHoOiCCIkQcdqbVCBbBNGXBkHJi3iWX8DnlblVaZGphy

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
-- Name: check_agent_commission_threshold(); Type: FUNCTION; Schema: public; Owner: doadmin
--

CREATE FUNCTION public.check_agent_commission_threshold() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- If paid_customers_count just reached 10, release commissions
    IF NEW.paid_customers_count >= 10 AND OLD.paid_customers_count < 10 THEN
        PERFORM release_pending_commissions(NEW.id);
        RAISE NOTICE 'Agent % reached 10 customers! Commissions released.', NEW.id;
    END IF;
    
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.check_agent_commission_threshold() OWNER TO doadmin;

--
-- Name: release_pending_commissions(integer); Type: FUNCTION; Schema: public; Owner: doadmin
--

CREATE FUNCTION public.release_pending_commissions(p_agent_id integer) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Update commissions to released status
    UPDATE commissions
    SET status = 'approved',
        released_at = CURRENT_TIMESTAMP,
        approved_at = CURRENT_TIMESTAMP
    WHERE agent_id = p_agent_id
    AND status = 'pending';
    
    -- Set can_withdraw flag
    UPDATE agents
    SET can_withdraw = TRUE
    WHERE id = p_agent_id;
    
    RAISE NOTICE 'Released pending commissions for agent %', p_agent_id;
END;
$$;


ALTER FUNCTION public.release_pending_commissions(p_agent_id integer) OWNER TO doadmin;

--
-- Name: FUNCTION release_pending_commissions(p_agent_id integer); Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON FUNCTION public.release_pending_commissions(p_agent_id integer) IS 'Release all pending commissions when agent reaches 10 customers';


--
-- Name: update_blog_posts_updated_at(); Type: FUNCTION; Schema: public; Owner: doadmin
--

CREATE FUNCTION public.update_blog_posts_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_blog_posts_updated_at() OWNER TO doadmin;

--
-- Name: update_faqs_updated_at(); Type: FUNCTION; Schema: public; Owner: doadmin
--

CREATE FUNCTION public.update_faqs_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_faqs_updated_at() OWNER TO doadmin;

--
-- Name: update_payment_approval_requests_updated_at(); Type: FUNCTION; Schema: public; Owner: doadmin
--

CREATE FUNCTION public.update_payment_approval_requests_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_payment_approval_requests_updated_at() OWNER TO doadmin;

--
-- Name: update_payment_methods_updated_at(); Type: FUNCTION; Schema: public; Owner: doadmin
--

CREATE FUNCTION public.update_payment_methods_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_payment_methods_updated_at() OWNER TO doadmin;

--
-- Name: update_support_tickets_updated_at(); Type: FUNCTION; Schema: public; Owner: doadmin
--

CREATE FUNCTION public.update_support_tickets_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_support_tickets_updated_at() OWNER TO doadmin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: affiliate_commissions; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.affiliate_commissions OWNER TO doadmin;

--
-- Name: affiliate_commissions_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.affiliate_commissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.affiliate_commissions_id_seq OWNER TO doadmin;

--
-- Name: affiliate_commissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.affiliate_commissions_id_seq OWNED BY public.affiliate_commissions.id;


--
-- Name: affiliate_links; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.affiliate_links OWNER TO doadmin;

--
-- Name: affiliate_links_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.affiliate_links_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.affiliate_links_id_seq OWNER TO doadmin;

--
-- Name: affiliate_links_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.affiliate_links_id_seq OWNED BY public.affiliate_links.id;


--
-- Name: affiliate_payouts; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.affiliate_payouts OWNER TO doadmin;

--
-- Name: affiliate_payouts_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.affiliate_payouts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.affiliate_payouts_id_seq OWNER TO doadmin;

--
-- Name: affiliate_payouts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.affiliate_payouts_id_seq OWNED BY public.affiliate_payouts.id;


--
-- Name: affiliate_referrals; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.affiliate_referrals OWNER TO doadmin;

--
-- Name: affiliate_referrals_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.affiliate_referrals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.affiliate_referrals_id_seq OWNER TO doadmin;

--
-- Name: affiliate_referrals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.affiliate_referrals_id_seq OWNED BY public.affiliate_referrals.id;


--
-- Name: affiliate_settings; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.affiliate_settings OWNER TO doadmin;

--
-- Name: affiliate_settings_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.affiliate_settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.affiliate_settings_id_seq OWNER TO doadmin;

--
-- Name: affiliate_settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.affiliate_settings_id_seq OWNED BY public.affiliate_settings.id;


--
-- Name: agents; Type: TABLE; Schema: public; Owner: doadmin
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
    updated_at timestamp without time zone NOT NULL,
    paid_customers_count integer DEFAULT 0 NOT NULL,
    can_withdraw boolean DEFAULT false NOT NULL,
    last_withdrawal_date timestamp without time zone
);


ALTER TABLE public.agents OWNER TO doadmin;

--
-- Name: COLUMN agents.pending_balance; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.agents.pending_balance IS 'Locked commissions waiting for 10-customer threshold (or available if threshold reached)';


--
-- Name: COLUMN agents.paid_customers_count; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.agents.paid_customers_count IS 'Number of customers who made a payment (for 10-customer threshold)';


--
-- Name: COLUMN agents.can_withdraw; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.agents.can_withdraw IS 'Whether agent has reached 10-customer threshold and can withdraw';


--
-- Name: COLUMN agents.last_withdrawal_date; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.agents.last_withdrawal_date IS 'Date of last withdrawal request (for 30-day cooldown)';


--
-- Name: commissions; Type: TABLE; Schema: public; Owner: doadmin
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
    admin_notes text,
    released_at timestamp without time zone,
    customer_id integer
);


ALTER TABLE public.commissions OWNER TO doadmin;

--
-- Name: COLUMN commissions.released_at; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.commissions.released_at IS 'When commission was released from pending (10-customer threshold reached)';


--
-- Name: COLUMN commissions.customer_id; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.commissions.customer_id IS 'Direct link to customer who made the purchase';


--
-- Name: agent_dashboard_stats; Type: VIEW; Schema: public; Owner: doadmin
--

CREATE VIEW public.agent_dashboard_stats AS
 SELECT a.id AS agent_id,
    a.user_id,
    a.agent_code,
    a.commission_rate,
    a.paid_customers_count,
    a.can_withdraw,
    a.pending_balance,
    a.total_earned,
    a.total_withdrawn,
    a.last_withdrawal_date,
        CASE
            WHEN (a.paid_customers_count >= 10) THEN a.pending_balance
            ELSE (0)::numeric
        END AS available_balance,
        CASE
            WHEN (a.paid_customers_count < 10) THEN a.pending_balance
            ELSE (0)::numeric
        END AS locked_balance,
    a.referral_count,
    a.active_referrals,
    COALESCE(pending_commissions.count, (0)::bigint) AS pending_commission_count,
    COALESCE(pending_commissions.amount, (0)::numeric) AS pending_commission_amount
   FROM (public.agents a
     LEFT JOIN ( SELECT commissions.agent_id,
            count(*) AS count,
            sum(commissions.commission_amount) AS amount
           FROM public.commissions
          WHERE ((commissions.status)::text = 'pending'::text)
          GROUP BY commissions.agent_id) pending_commissions ON ((a.id = pending_commissions.agent_id)));


ALTER VIEW public.agent_dashboard_stats OWNER TO doadmin;

--
-- Name: VIEW agent_dashboard_stats; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON VIEW public.agent_dashboard_stats IS 'Comprehensive agent statistics for dashboard';


--
-- Name: agents_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.agents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.agents_id_seq OWNER TO doadmin;

--
-- Name: agents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.agents_id_seq OWNED BY public.agents.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: doadmin
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO doadmin;

--
-- Name: blog_posts; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.blog_posts OWNER TO doadmin;

--
-- Name: TABLE blog_posts; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON TABLE public.blog_posts IS 'Blog posts for content management system';


--
-- Name: COLUMN blog_posts.slug; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.blog_posts.slug IS 'URL-friendly unique identifier for the post';


--
-- Name: COLUMN blog_posts.status; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.blog_posts.status IS 'Post status: draft, published, or archived';


--
-- Name: COLUMN blog_posts.featured; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.blog_posts.featured IS 'Whether the post should be featured on the homepage';


--
-- Name: COLUMN blog_posts.reading_time; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.blog_posts.reading_time IS 'Estimated reading time in minutes';


--
-- Name: blog_posts_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.blog_posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.blog_posts_id_seq OWNER TO doadmin;

--
-- Name: blog_posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.blog_posts_id_seq OWNED BY public.blog_posts.id;


--
-- Name: challenges; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.challenges OWNER TO doadmin;

--
-- Name: COLUMN challenges.payment_type; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.challenges.payment_type IS 'credit_card, cash, free';


--
-- Name: COLUMN challenges.approval_status; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.challenges.approval_status IS 'pending, approved, rejected (only for cash/free payments)';


--
-- Name: challenges_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.challenges_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.challenges_id_seq OWNER TO doadmin;

--
-- Name: challenges_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.challenges_id_seq OWNED BY public.challenges.id;


--
-- Name: commission_balances; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.commission_balances OWNER TO doadmin;

--
-- Name: TABLE commission_balances; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON TABLE public.commission_balances IS 'Cached commission balances for performance';


--
-- Name: commission_balances_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.commission_balances_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.commission_balances_id_seq OWNER TO doadmin;

--
-- Name: commission_balances_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.commission_balances_id_seq OWNED BY public.commission_balances.id;


--
-- Name: commission_rules; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.commission_rules OWNER TO doadmin;

--
-- Name: TABLE commission_rules; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON TABLE public.commission_rules IS 'Commission calculation rules for MLM system';


--
-- Name: commission_rules_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.commission_rules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.commission_rules_id_seq OWNER TO doadmin;

--
-- Name: commission_rules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.commission_rules_id_seq OWNED BY public.commission_rules.id;


--
-- Name: commission_withdrawals; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.commission_withdrawals OWNER TO doadmin;

--
-- Name: TABLE commission_withdrawals; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON TABLE public.commission_withdrawals IS 'Commission withdrawal requests';


--
-- Name: commission_withdrawals_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.commission_withdrawals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.commission_withdrawals_id_seq OWNER TO doadmin;

--
-- Name: commission_withdrawals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.commission_withdrawals_id_seq OWNED BY public.commission_withdrawals.id;


--
-- Name: commissions_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.commissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.commissions_id_seq OWNER TO doadmin;

--
-- Name: commissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.commissions_id_seq OWNED BY public.commissions.id;


--
-- Name: course_enrollments; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.course_enrollments OWNER TO doadmin;

--
-- Name: course_enrollments_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.course_enrollments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.course_enrollments_id_seq OWNER TO doadmin;

--
-- Name: course_enrollments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.course_enrollments_id_seq OWNED BY public.course_enrollments.id;


--
-- Name: email_queue; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.email_queue OWNER TO doadmin;

--
-- Name: email_queue_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.email_queue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.email_queue_id_seq OWNER TO doadmin;

--
-- Name: email_queue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.email_queue_id_seq OWNED BY public.email_queue.id;


--
-- Name: email_verification_tokens; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.email_verification_tokens OWNER TO doadmin;

--
-- Name: email_verification_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.email_verification_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.email_verification_tokens_id_seq OWNER TO doadmin;

--
-- Name: email_verification_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.email_verification_tokens_id_seq OWNED BY public.email_verification_tokens.id;


--
-- Name: faqs; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.faqs OWNER TO doadmin;

--
-- Name: faqs_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.faqs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.faqs_id_seq OWNER TO doadmin;

--
-- Name: faqs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.faqs_id_seq OWNED BY public.faqs.id;


--
-- Name: lead_activities; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.lead_activities OWNER TO doadmin;

--
-- Name: lead_activities_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.lead_activities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.lead_activities_id_seq OWNER TO doadmin;

--
-- Name: lead_activities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.lead_activities_id_seq OWNED BY public.lead_activities.id;


--
-- Name: lead_notes; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.lead_notes OWNER TO doadmin;

--
-- Name: lead_notes_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.lead_notes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.lead_notes_id_seq OWNER TO doadmin;

--
-- Name: lead_notes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.lead_notes_id_seq OWNED BY public.lead_notes.id;


--
-- Name: leads; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.leads OWNER TO doadmin;

--
-- Name: leads_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.leads_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.leads_id_seq OWNER TO doadmin;

--
-- Name: leads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.leads_id_seq OWNED BY public.leads.id;


--
-- Name: notification_preferences; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.notification_preferences OWNER TO doadmin;

--
-- Name: notification_preferences_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.notification_preferences_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notification_preferences_id_seq OWNER TO doadmin;

--
-- Name: notification_preferences_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.notification_preferences_id_seq OWNED BY public.notification_preferences.id;


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.notifications OWNER TO doadmin;

--
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notifications_id_seq OWNER TO doadmin;

--
-- Name: notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;


--
-- Name: password_reset_tokens; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.password_reset_tokens OWNER TO doadmin;

--
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.password_reset_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.password_reset_tokens_id_seq OWNER TO doadmin;

--
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.password_reset_tokens_id_seq OWNED BY public.password_reset_tokens.id;


--
-- Name: payment_approval_requests; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.payment_approval_requests OWNER TO doadmin;

--
-- Name: payment_approval_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.payment_approval_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payment_approval_requests_id_seq OWNER TO doadmin;

--
-- Name: payment_approval_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.payment_approval_requests_id_seq OWNED BY public.payment_approval_requests.id;


--
-- Name: payment_methods; Type: TABLE; Schema: public; Owner: doadmin
--

CREATE TABLE public.payment_methods (
    id integer NOT NULL,
    user_id integer NOT NULL,
    method_type character varying(20) NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    bank_name character varying(100),
    account_number character varying(100),
    branch_number character varying(20),
    account_holder_name character varying(100),
    paypal_email character varying(100),
    crypto_address character varying(200),
    crypto_network character varying(20),
    wise_email character varying(100),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT payment_methods_crypto_network_check CHECK (((crypto_network)::text = ANY ((ARRAY['TRC20'::character varying, 'ERC20'::character varying, 'BEP20'::character varying, NULL::character varying])::text[]))),
    CONSTRAINT payment_methods_method_type_check CHECK (((method_type)::text = ANY ((ARRAY['bank'::character varying, 'paypal'::character varying, 'crypto'::character varying, 'wise'::character varying])::text[])))
);


ALTER TABLE public.payment_methods OWNER TO doadmin;

--
-- Name: TABLE payment_methods; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON TABLE public.payment_methods IS 'User payment methods for commission withdrawals';


--
-- Name: COLUMN payment_methods.method_type; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.payment_methods.method_type IS 'Payment method: bank, paypal, crypto, wise';


--
-- Name: COLUMN payment_methods.is_active; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.payment_methods.is_active IS 'Only one active method per user allowed';


--
-- Name: payment_methods_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.payment_methods_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payment_methods_id_seq OWNER TO doadmin;

--
-- Name: payment_methods_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.payment_methods_id_seq OWNED BY public.payment_methods.id;


--
-- Name: payments; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.payments OWNER TO doadmin;

--
-- Name: COLUMN payments.payment_type; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.payments.payment_type IS 'credit_card, cash, free';


--
-- Name: COLUMN payments.approval_status; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.payments.approval_status IS 'pending, approved, rejected (only for cash/free payments)';


--
-- Name: payments_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.payments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payments_id_seq OWNER TO doadmin;

--
-- Name: payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.payments_id_seq OWNED BY public.payments.id;


--
-- Name: program_addons; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.program_addons OWNER TO doadmin;

--
-- Name: program_addons_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.program_addons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.program_addons_id_seq OWNER TO doadmin;

--
-- Name: program_addons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.program_addons_id_seq OWNED BY public.program_addons.id;


--
-- Name: referrals; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.referrals OWNER TO doadmin;

--
-- Name: referrals_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.referrals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.referrals_id_seq OWNER TO doadmin;

--
-- Name: referrals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.referrals_id_seq OWNED BY public.referrals.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.roles OWNER TO doadmin;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_seq OWNER TO doadmin;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: support_articles; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.support_articles OWNER TO doadmin;

--
-- Name: support_articles_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.support_articles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.support_articles_id_seq OWNER TO doadmin;

--
-- Name: support_articles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.support_articles_id_seq OWNED BY public.support_articles.id;


--
-- Name: support_tickets; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.support_tickets OWNER TO doadmin;

--
-- Name: support_tickets_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.support_tickets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.support_tickets_id_seq OWNER TO doadmin;

--
-- Name: support_tickets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.support_tickets_id_seq OWNED BY public.support_tickets.id;


--
-- Name: tenants; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.tenants OWNER TO doadmin;

--
-- Name: tenants_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.tenants_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tenants_id_seq OWNER TO doadmin;

--
-- Name: tenants_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.tenants_id_seq OWNED BY public.tenants.id;


--
-- Name: ticket_messages; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.ticket_messages OWNER TO doadmin;

--
-- Name: ticket_messages_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.ticket_messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ticket_messages_id_seq OWNER TO doadmin;

--
-- Name: ticket_messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.ticket_messages_id_seq OWNED BY public.ticket_messages.id;


--
-- Name: trades; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.trades OWNER TO doadmin;

--
-- Name: trades_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.trades_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trades_id_seq OWNER TO doadmin;

--
-- Name: trades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.trades_id_seq OWNED BY public.trades.id;


--
-- Name: trading_programs; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.trading_programs OWNER TO doadmin;

--
-- Name: trading_programs_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.trading_programs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trading_programs_id_seq OWNER TO doadmin;

--
-- Name: trading_programs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.trading_programs_id_seq OWNED BY public.trading_programs.id;


--
-- Name: transactions; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.transactions OWNER TO doadmin;

--
-- Name: transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.transactions_id_seq OWNER TO doadmin;

--
-- Name: transactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.transactions_id_seq OWNED BY public.transactions.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.users OWNER TO doadmin;

--
-- Name: COLUMN users.referral_code; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.users.referral_code IS 'Unique referral code for this user (agents/masters/supermasters)';


--
-- Name: COLUMN users.referred_by_code; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.users.referred_by_code IS 'Referral code used when signing up';


--
-- Name: COLUMN users.referred_by_user_id; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.users.referred_by_user_id IS 'User ID who referred this user';


--
-- Name: COLUMN users.has_purchased_program; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.users.has_purchased_program IS 'Whether user has purchased any program';


--
-- Name: COLUMN users.first_purchase_at; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.users.first_purchase_at IS 'Timestamp of first program purchase';


--
-- Name: COLUMN users.total_purchases; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.users.total_purchases IS 'Total number of programs purchased';


--
-- Name: COLUMN users.total_referrals; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.users.total_referrals IS 'Total number of users referred';


--
-- Name: COLUMN users.active_referrals; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.users.active_referrals IS 'Number of active referred users';


--
-- Name: COLUMN users.referral_earnings; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON COLUMN public.users.referral_earnings IS 'Total earnings from referrals';


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO doadmin;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: verification_attempts; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.verification_attempts OWNER TO doadmin;

--
-- Name: verification_attempts_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.verification_attempts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.verification_attempts_id_seq OWNER TO doadmin;

--
-- Name: verification_attempts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.verification_attempts_id_seq OWNED BY public.verification_attempts.id;


--
-- Name: wallets; Type: TABLE; Schema: public; Owner: doadmin
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


ALTER TABLE public.wallets OWNER TO doadmin;

--
-- Name: wallets_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.wallets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.wallets_id_seq OWNER TO doadmin;

--
-- Name: wallets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.wallets_id_seq OWNED BY public.wallets.id;


--
-- Name: withdrawals; Type: TABLE; Schema: public; Owner: doadmin
--

CREATE TABLE public.withdrawals (
    id integer NOT NULL,
    agent_id integer NOT NULL,
    amount numeric(12,2) NOT NULL,
    fee numeric(12,2) NOT NULL,
    net_amount numeric(12,2) NOT NULL,
    payment_method character varying(50) NOT NULL,
    payment_details jsonb,
    status character varying(20) NOT NULL,
    approved_by integer,
    approved_at timestamp without time zone,
    processed_at timestamp without time zone,
    completed_at timestamp without time zone,
    transaction_id character varying(100),
    rejection_reason text,
    notes text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    requested_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.withdrawals OWNER TO doadmin;

--
-- Name: withdrawals_id_seq; Type: SEQUENCE; Schema: public; Owner: doadmin
--

CREATE SEQUENCE public.withdrawals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.withdrawals_id_seq OWNER TO doadmin;

--
-- Name: withdrawals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doadmin
--

ALTER SEQUENCE public.withdrawals_id_seq OWNED BY public.withdrawals.id;


--
-- Name: affiliate_commissions id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_commissions ALTER COLUMN id SET DEFAULT nextval('public.affiliate_commissions_id_seq'::regclass);


--
-- Name: affiliate_links id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_links ALTER COLUMN id SET DEFAULT nextval('public.affiliate_links_id_seq'::regclass);


--
-- Name: affiliate_payouts id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_payouts ALTER COLUMN id SET DEFAULT nextval('public.affiliate_payouts_id_seq'::regclass);


--
-- Name: affiliate_referrals id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_referrals ALTER COLUMN id SET DEFAULT nextval('public.affiliate_referrals_id_seq'::regclass);


--
-- Name: affiliate_settings id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_settings ALTER COLUMN id SET DEFAULT nextval('public.affiliate_settings_id_seq'::regclass);


--
-- Name: agents id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.agents ALTER COLUMN id SET DEFAULT nextval('public.agents_id_seq'::regclass);


--
-- Name: blog_posts id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.blog_posts ALTER COLUMN id SET DEFAULT nextval('public.blog_posts_id_seq'::regclass);


--
-- Name: challenges id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.challenges ALTER COLUMN id SET DEFAULT nextval('public.challenges_id_seq'::regclass);


--
-- Name: commission_balances id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commission_balances ALTER COLUMN id SET DEFAULT nextval('public.commission_balances_id_seq'::regclass);


--
-- Name: commission_rules id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commission_rules ALTER COLUMN id SET DEFAULT nextval('public.commission_rules_id_seq'::regclass);


--
-- Name: commission_withdrawals id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commission_withdrawals ALTER COLUMN id SET DEFAULT nextval('public.commission_withdrawals_id_seq'::regclass);


--
-- Name: commissions id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commissions ALTER COLUMN id SET DEFAULT nextval('public.commissions_id_seq'::regclass);


--
-- Name: course_enrollments id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.course_enrollments ALTER COLUMN id SET DEFAULT nextval('public.course_enrollments_id_seq'::regclass);


--
-- Name: email_queue id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.email_queue ALTER COLUMN id SET DEFAULT nextval('public.email_queue_id_seq'::regclass);


--
-- Name: email_verification_tokens id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.email_verification_tokens ALTER COLUMN id SET DEFAULT nextval('public.email_verification_tokens_id_seq'::regclass);


--
-- Name: faqs id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.faqs ALTER COLUMN id SET DEFAULT nextval('public.faqs_id_seq'::regclass);


--
-- Name: lead_activities id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.lead_activities ALTER COLUMN id SET DEFAULT nextval('public.lead_activities_id_seq'::regclass);


--
-- Name: lead_notes id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.lead_notes ALTER COLUMN id SET DEFAULT nextval('public.lead_notes_id_seq'::regclass);


--
-- Name: leads id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.leads ALTER COLUMN id SET DEFAULT nextval('public.leads_id_seq'::regclass);


--
-- Name: notification_preferences id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.notification_preferences ALTER COLUMN id SET DEFAULT nextval('public.notification_preferences_id_seq'::regclass);


--
-- Name: notifications id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);


--
-- Name: password_reset_tokens id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.password_reset_tokens ALTER COLUMN id SET DEFAULT nextval('public.password_reset_tokens_id_seq'::regclass);


--
-- Name: payment_approval_requests id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.payment_approval_requests ALTER COLUMN id SET DEFAULT nextval('public.payment_approval_requests_id_seq'::regclass);


--
-- Name: payment_methods id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.payment_methods ALTER COLUMN id SET DEFAULT nextval('public.payment_methods_id_seq'::regclass);


--
-- Name: payments id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.payments ALTER COLUMN id SET DEFAULT nextval('public.payments_id_seq'::regclass);


--
-- Name: program_addons id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.program_addons ALTER COLUMN id SET DEFAULT nextval('public.program_addons_id_seq'::regclass);


--
-- Name: referrals id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.referrals ALTER COLUMN id SET DEFAULT nextval('public.referrals_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: support_articles id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.support_articles ALTER COLUMN id SET DEFAULT nextval('public.support_articles_id_seq'::regclass);


--
-- Name: support_tickets id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.support_tickets ALTER COLUMN id SET DEFAULT nextval('public.support_tickets_id_seq'::regclass);


--
-- Name: tenants id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.tenants ALTER COLUMN id SET DEFAULT nextval('public.tenants_id_seq'::regclass);


--
-- Name: ticket_messages id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.ticket_messages ALTER COLUMN id SET DEFAULT nextval('public.ticket_messages_id_seq'::regclass);


--
-- Name: trades id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.trades ALTER COLUMN id SET DEFAULT nextval('public.trades_id_seq'::regclass);


--
-- Name: trading_programs id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.trading_programs ALTER COLUMN id SET DEFAULT nextval('public.trading_programs_id_seq'::regclass);


--
-- Name: transactions id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.transactions ALTER COLUMN id SET DEFAULT nextval('public.transactions_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: verification_attempts id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.verification_attempts ALTER COLUMN id SET DEFAULT nextval('public.verification_attempts_id_seq'::regclass);


--
-- Name: wallets id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.wallets ALTER COLUMN id SET DEFAULT nextval('public.wallets_id_seq'::regclass);


--
-- Name: withdrawals id; Type: DEFAULT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.withdrawals ALTER COLUMN id SET DEFAULT nextval('public.withdrawals_id_seq'::regclass);


--
-- Name: affiliate_commissions affiliate_commissions_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_commissions
    ADD CONSTRAINT affiliate_commissions_pkey PRIMARY KEY (id);


--
-- Name: affiliate_links affiliate_links_code_key; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_links
    ADD CONSTRAINT affiliate_links_code_key UNIQUE (code);


--
-- Name: affiliate_links affiliate_links_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_links
    ADD CONSTRAINT affiliate_links_pkey PRIMARY KEY (id);


--
-- Name: affiliate_payouts affiliate_payouts_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_payouts
    ADD CONSTRAINT affiliate_payouts_pkey PRIMARY KEY (id);


--
-- Name: affiliate_referrals affiliate_referrals_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_referrals
    ADD CONSTRAINT affiliate_referrals_pkey PRIMARY KEY (id);


--
-- Name: affiliate_settings affiliate_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_settings
    ADD CONSTRAINT affiliate_settings_pkey PRIMARY KEY (id);


--
-- Name: agents agents_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.agents
    ADD CONSTRAINT agents_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: blog_posts blog_posts_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.blog_posts
    ADD CONSTRAINT blog_posts_pkey PRIMARY KEY (id);


--
-- Name: blog_posts blog_posts_slug_key; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.blog_posts
    ADD CONSTRAINT blog_posts_slug_key UNIQUE (slug);


--
-- Name: challenges challenges_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.challenges
    ADD CONSTRAINT challenges_pkey PRIMARY KEY (id);


--
-- Name: commission_balances commission_balances_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commission_balances
    ADD CONSTRAINT commission_balances_pkey PRIMARY KEY (id);


--
-- Name: commission_balances commission_balances_user_id_key; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commission_balances
    ADD CONSTRAINT commission_balances_user_id_key UNIQUE (user_id);


--
-- Name: commission_rules commission_rules_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commission_rules
    ADD CONSTRAINT commission_rules_pkey PRIMARY KEY (id);


--
-- Name: commission_withdrawals commission_withdrawals_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commission_withdrawals
    ADD CONSTRAINT commission_withdrawals_pkey PRIMARY KEY (id);


--
-- Name: commissions commissions_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commissions
    ADD CONSTRAINT commissions_pkey PRIMARY KEY (id);


--
-- Name: course_enrollments course_enrollments_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.course_enrollments
    ADD CONSTRAINT course_enrollments_pkey PRIMARY KEY (id);


--
-- Name: email_queue email_queue_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.email_queue
    ADD CONSTRAINT email_queue_pkey PRIMARY KEY (id);


--
-- Name: email_verification_tokens email_verification_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.email_verification_tokens
    ADD CONSTRAINT email_verification_tokens_pkey PRIMARY KEY (id);


--
-- Name: faqs faqs_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.faqs
    ADD CONSTRAINT faqs_pkey PRIMARY KEY (id);


--
-- Name: lead_activities lead_activities_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.lead_activities
    ADD CONSTRAINT lead_activities_pkey PRIMARY KEY (id);


--
-- Name: lead_notes lead_notes_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.lead_notes
    ADD CONSTRAINT lead_notes_pkey PRIMARY KEY (id);


--
-- Name: leads leads_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.leads
    ADD CONSTRAINT leads_pkey PRIMARY KEY (id);


--
-- Name: notification_preferences notification_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.notification_preferences
    ADD CONSTRAINT notification_preferences_pkey PRIMARY KEY (id);


--
-- Name: notification_preferences notification_preferences_user_id_key; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.notification_preferences
    ADD CONSTRAINT notification_preferences_user_id_key UNIQUE (user_id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: password_reset_tokens password_reset_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_pkey PRIMARY KEY (id);


--
-- Name: payment_approval_requests payment_approval_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.payment_approval_requests
    ADD CONSTRAINT payment_approval_requests_pkey PRIMARY KEY (id);


--
-- Name: payment_methods payment_methods_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.payment_methods
    ADD CONSTRAINT payment_methods_pkey PRIMARY KEY (id);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- Name: payments payments_transaction_id_key; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_transaction_id_key UNIQUE (transaction_id);


--
-- Name: program_addons program_addons_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.program_addons
    ADD CONSTRAINT program_addons_pkey PRIMARY KEY (id);


--
-- Name: referrals referrals_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT referrals_pkey PRIMARY KEY (id);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: support_articles support_articles_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.support_articles
    ADD CONSTRAINT support_articles_pkey PRIMARY KEY (id);


--
-- Name: support_articles support_articles_slug_key; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.support_articles
    ADD CONSTRAINT support_articles_slug_key UNIQUE (slug);


--
-- Name: support_tickets support_tickets_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.support_tickets
    ADD CONSTRAINT support_tickets_pkey PRIMARY KEY (id);


--
-- Name: support_tickets support_tickets_ticket_number_key; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.support_tickets
    ADD CONSTRAINT support_tickets_ticket_number_key UNIQUE (ticket_number);


--
-- Name: tenants tenants_custom_domain_key; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.tenants
    ADD CONSTRAINT tenants_custom_domain_key UNIQUE (custom_domain);


--
-- Name: tenants tenants_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.tenants
    ADD CONSTRAINT tenants_pkey PRIMARY KEY (id);


--
-- Name: ticket_messages ticket_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.ticket_messages
    ADD CONSTRAINT ticket_messages_pkey PRIMARY KEY (id);


--
-- Name: trades trades_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.trades
    ADD CONSTRAINT trades_pkey PRIMARY KEY (id);


--
-- Name: trades trades_ticket_key; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.trades
    ADD CONSTRAINT trades_ticket_key UNIQUE (ticket);


--
-- Name: trading_programs trading_programs_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.trading_programs
    ADD CONSTRAINT trading_programs_pkey PRIMARY KEY (id);


--
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);


--
-- Name: course_enrollments unique_course_email; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.course_enrollments
    ADD CONSTRAINT unique_course_email UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_referral_code_key; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_referral_code_key UNIQUE (referral_code);


--
-- Name: verification_attempts verification_attempts_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.verification_attempts
    ADD CONSTRAINT verification_attempts_pkey PRIMARY KEY (id);


--
-- Name: wallets wallets_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.wallets
    ADD CONSTRAINT wallets_pkey PRIMARY KEY (id);


--
-- Name: wallets wallets_user_id_key; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.wallets
    ADD CONSTRAINT wallets_user_id_key UNIQUE (user_id);


--
-- Name: withdrawals withdrawals_pkey; Type: CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.withdrawals
    ADD CONSTRAINT withdrawals_pkey PRIMARY KEY (id);


--
-- Name: idx_affiliate_commissions_affiliate_user; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_affiliate_commissions_affiliate_user ON public.affiliate_commissions USING btree (affiliate_user_id);


--
-- Name: idx_affiliate_commissions_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_affiliate_commissions_status ON public.affiliate_commissions USING btree (status);


--
-- Name: idx_affiliate_links_code; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_affiliate_links_code ON public.affiliate_links USING btree (code);


--
-- Name: idx_affiliate_links_user_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_affiliate_links_user_id ON public.affiliate_links USING btree (user_id);


--
-- Name: idx_affiliate_payouts_affiliate_user; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_affiliate_payouts_affiliate_user ON public.affiliate_payouts USING btree (affiliate_user_id);


--
-- Name: idx_affiliate_payouts_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_affiliate_payouts_status ON public.affiliate_payouts USING btree (status);


--
-- Name: idx_affiliate_referrals_affiliate_link; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_affiliate_referrals_affiliate_link ON public.affiliate_referrals USING btree (affiliate_link_id);


--
-- Name: idx_affiliate_referrals_affiliate_user; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_affiliate_referrals_affiliate_user ON public.affiliate_referrals USING btree (affiliate_user_id);


--
-- Name: idx_affiliate_referrals_referred_user; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_affiliate_referrals_referred_user ON public.affiliate_referrals USING btree (referred_user_id);


--
-- Name: idx_affiliate_referrals_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_affiliate_referrals_status ON public.affiliate_referrals USING btree (status);


--
-- Name: idx_approval_requests_challenge_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_approval_requests_challenge_id ON public.payment_approval_requests USING btree (challenge_id);


--
-- Name: idx_approval_requests_requested_by; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_approval_requests_requested_by ON public.payment_approval_requests USING btree (requested_by);


--
-- Name: idx_approval_requests_requested_for; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_approval_requests_requested_for ON public.payment_approval_requests USING btree (requested_for);


--
-- Name: idx_approval_requests_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_approval_requests_status ON public.payment_approval_requests USING btree (status);


--
-- Name: idx_blog_category_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_blog_category_status ON public.blog_posts USING btree (category, status);


--
-- Name: idx_blog_featured_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_blog_featured_status ON public.blog_posts USING btree (featured, status);


--
-- Name: idx_blog_posts_author_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_blog_posts_author_id ON public.blog_posts USING btree (author_id);


--
-- Name: idx_blog_posts_category; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_blog_posts_category ON public.blog_posts USING btree (category);


--
-- Name: idx_blog_posts_featured; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_blog_posts_featured ON public.blog_posts USING btree (featured);


--
-- Name: idx_blog_posts_published_at; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_blog_posts_published_at ON public.blog_posts USING btree (published_at);


--
-- Name: idx_blog_posts_search; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_blog_posts_search ON public.blog_posts USING gin (to_tsvector('english'::regconfig, (((((title)::text || ' '::text) || COALESCE(excerpt, ''::text)) || ' '::text) || COALESCE(content, ''::text))));


--
-- Name: idx_blog_posts_slug; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_blog_posts_slug ON public.blog_posts USING btree (slug);


--
-- Name: idx_blog_posts_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_blog_posts_status ON public.blog_posts USING btree (status);


--
-- Name: idx_blog_status_published; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_blog_status_published ON public.blog_posts USING btree (status, published_at);


--
-- Name: idx_challenges_approval_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_challenges_approval_status ON public.challenges USING btree (approval_status);


--
-- Name: idx_challenges_created_by; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_challenges_created_by ON public.challenges USING btree (created_by);


--
-- Name: idx_challenges_payment_type; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_challenges_payment_type ON public.challenges USING btree (payment_type);


--
-- Name: idx_commission_balances_user_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_commission_balances_user_id ON public.commission_balances USING btree (user_id);


--
-- Name: idx_commission_rules_active; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_commission_rules_active ON public.commission_rules USING btree (is_active);


--
-- Name: idx_commission_rules_role; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_commission_rules_role ON public.commission_rules USING btree (target_role);


--
-- Name: idx_commission_rules_type; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_commission_rules_type ON public.commission_rules USING btree (rule_type);


--
-- Name: idx_commission_withdrawals_requested_at; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_commission_withdrawals_requested_at ON public.commission_withdrawals USING btree (requested_at);


--
-- Name: idx_commission_withdrawals_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_commission_withdrawals_status ON public.commission_withdrawals USING btree (status);


--
-- Name: idx_commission_withdrawals_user_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_commission_withdrawals_user_id ON public.commission_withdrawals USING btree (user_id);


--
-- Name: idx_commissions_customer_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_commissions_customer_id ON public.commissions USING btree (customer_id);


--
-- Name: idx_commissions_level; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_commissions_level ON public.commissions USING btree (level);


--
-- Name: idx_commissions_source_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_commissions_source_id ON public.commissions USING btree (source_id);


--
-- Name: idx_commissions_source_type; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_commissions_source_type ON public.commissions USING btree (source_type);


--
-- Name: idx_commissions_source_user_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_commissions_source_user_id ON public.commissions USING btree (source_user_id);


--
-- Name: idx_commissions_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_commissions_status ON public.commissions USING btree (status);


--
-- Name: idx_commissions_user_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_commissions_user_id ON public.commissions USING btree (user_id);


--
-- Name: idx_course_enrollments_email; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_course_enrollments_email ON public.course_enrollments USING btree (email);


--
-- Name: idx_course_enrollments_enrolled_at; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_course_enrollments_enrolled_at ON public.course_enrollments USING btree (enrolled_at);


--
-- Name: idx_course_enrollments_unsubscribed; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_course_enrollments_unsubscribed ON public.course_enrollments USING btree (unsubscribed);


--
-- Name: idx_email_created; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_email_created ON public.verification_attempts USING btree (email, created_at);


--
-- Name: idx_email_queue_created_at; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_email_queue_created_at ON public.email_queue USING btree (created_at);


--
-- Name: idx_email_queue_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_email_queue_status ON public.email_queue USING btree (status);


--
-- Name: idx_faqs_category; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_faqs_category ON public.faqs USING btree (category);


--
-- Name: idx_faqs_category_order; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_faqs_category_order ON public.faqs USING btree (category, "order");


--
-- Name: idx_faqs_is_featured; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_faqs_is_featured ON public.faqs USING btree (is_featured);


--
-- Name: idx_faqs_is_published; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_faqs_is_published ON public.faqs USING btree (is_published);


--
-- Name: idx_faqs_order; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_faqs_order ON public.faqs USING btree ("order");


--
-- Name: idx_ip_created; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_ip_created ON public.verification_attempts USING btree (ip_address, created_at);


--
-- Name: idx_notifications_created_at; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_notifications_created_at ON public.notifications USING btree (created_at);


--
-- Name: idx_notifications_is_read; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_notifications_is_read ON public.notifications USING btree (is_read);


--
-- Name: idx_notifications_type; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_notifications_type ON public.notifications USING btree (type);


--
-- Name: idx_notifications_user_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_notifications_user_id ON public.notifications USING btree (user_id);


--
-- Name: idx_payment_methods_user_active; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_payment_methods_user_active ON public.payment_methods USING btree (user_id, is_active);


--
-- Name: idx_payments_approval_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_payments_approval_status ON public.payments USING btree (approval_status);


--
-- Name: idx_payments_payment_type; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_payments_payment_type ON public.payments USING btree (payment_type);


--
-- Name: idx_success_created; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_success_created ON public.verification_attempts USING btree (success, created_at);


--
-- Name: idx_support_articles_category; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_support_articles_category ON public.support_articles USING btree (category);


--
-- Name: idx_support_articles_featured; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_support_articles_featured ON public.support_articles USING btree (featured);


--
-- Name: idx_support_articles_published_at; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_support_articles_published_at ON public.support_articles USING btree (published_at);


--
-- Name: idx_support_articles_search; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_support_articles_search ON public.support_articles USING gin (to_tsvector('english'::regconfig, (((title)::text || ' '::text) || content)));


--
-- Name: idx_support_articles_slug; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_support_articles_slug ON public.support_articles USING btree (slug);


--
-- Name: idx_support_articles_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_support_articles_status ON public.support_articles USING btree (status);


--
-- Name: idx_support_tickets_assigned_to; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_support_tickets_assigned_to ON public.support_tickets USING btree (assigned_to);


--
-- Name: idx_support_tickets_category; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_support_tickets_category ON public.support_tickets USING btree (category);


--
-- Name: idx_support_tickets_created_at; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_support_tickets_created_at ON public.support_tickets USING btree (created_at DESC);


--
-- Name: idx_support_tickets_email; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_support_tickets_email ON public.support_tickets USING btree (email);


--
-- Name: idx_support_tickets_priority; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_support_tickets_priority ON public.support_tickets USING btree (priority);


--
-- Name: idx_support_tickets_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_support_tickets_status ON public.support_tickets USING btree (status);


--
-- Name: idx_support_tickets_status_priority; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_support_tickets_status_priority ON public.support_tickets USING btree (status, priority);


--
-- Name: idx_support_tickets_ticket_number; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_support_tickets_ticket_number ON public.support_tickets USING btree (ticket_number);


--
-- Name: idx_support_tickets_user_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_support_tickets_user_id ON public.support_tickets USING btree (user_id);


--
-- Name: idx_ticket_messages_created_at; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_ticket_messages_created_at ON public.ticket_messages USING btree (created_at DESC);


--
-- Name: idx_ticket_messages_is_staff; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_ticket_messages_is_staff ON public.ticket_messages USING btree (is_staff);


--
-- Name: idx_ticket_messages_ticket_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_ticket_messages_ticket_id ON public.ticket_messages USING btree (ticket_id);


--
-- Name: idx_ticket_messages_user_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_ticket_messages_user_id ON public.ticket_messages USING btree (user_id);


--
-- Name: idx_users_referral_code; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_users_referral_code ON public.users USING btree (referral_code);


--
-- Name: idx_users_referred_by_code; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_users_referred_by_code ON public.users USING btree (referred_by_code);


--
-- Name: idx_users_referred_by_user_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX idx_users_referred_by_user_id ON public.users USING btree (referred_by_user_id);


--
-- Name: ix_agents_agent_code; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE UNIQUE INDEX ix_agents_agent_code ON public.agents USING btree (agent_code);


--
-- Name: ix_challenge_created_at; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_challenge_created_at ON public.challenges USING btree (created_at);


--
-- Name: ix_challenge_program_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_challenge_program_id ON public.challenges USING btree (program_id);


--
-- Name: ix_challenge_user_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_challenge_user_status ON public.challenges USING btree (user_id, status);


--
-- Name: ix_commission_agent_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_commission_agent_status ON public.commissions USING btree (agent_id, status);


--
-- Name: ix_commission_created_at; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_commission_created_at ON public.commissions USING btree (created_at);


--
-- Name: ix_email_verification_tokens_code; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_email_verification_tokens_code ON public.email_verification_tokens USING btree (code);


--
-- Name: ix_email_verification_tokens_token; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE UNIQUE INDEX ix_email_verification_tokens_token ON public.email_verification_tokens USING btree (token);


--
-- Name: ix_lead_activities_activity_type; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_lead_activities_activity_type ON public.lead_activities USING btree (activity_type);


--
-- Name: ix_lead_activities_lead_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_lead_activities_lead_id ON public.lead_activities USING btree (lead_id);


--
-- Name: ix_lead_notes_lead_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_lead_notes_lead_id ON public.lead_notes USING btree (lead_id);


--
-- Name: ix_leads_assigned_to; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_leads_assigned_to ON public.leads USING btree (assigned_to);


--
-- Name: ix_leads_email; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_leads_email ON public.leads USING btree (email);


--
-- Name: ix_leads_next_follow_up; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_leads_next_follow_up ON public.leads USING btree (next_follow_up);


--
-- Name: ix_leads_source; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_leads_source ON public.leads USING btree (source);


--
-- Name: ix_leads_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_leads_status ON public.leads USING btree (status);


--
-- Name: ix_password_reset_tokens_code; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_password_reset_tokens_code ON public.password_reset_tokens USING btree (code);


--
-- Name: ix_password_reset_tokens_token; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE UNIQUE INDEX ix_password_reset_tokens_token ON public.password_reset_tokens USING btree (token);


--
-- Name: ix_referral_agent_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_referral_agent_id ON public.referrals USING btree (agent_id);


--
-- Name: ix_referral_status; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_referral_status ON public.referrals USING btree (status);


--
-- Name: ix_referrals_referral_code; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_referrals_referral_code ON public.referrals USING btree (referral_code);


--
-- Name: ix_tenants_subdomain; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE UNIQUE INDEX ix_tenants_subdomain ON public.tenants USING btree (subdomain);


--
-- Name: ix_transaction_created_at; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_transaction_created_at ON public.transactions USING btree (created_at);


--
-- Name: ix_transaction_type; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_transaction_type ON public.transactions USING btree (type);


--
-- Name: ix_transaction_wallet_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_transaction_wallet_id ON public.transactions USING btree (wallet_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_level; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_users_level ON public.users USING btree (level);


--
-- Name: ix_users_parent_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_users_parent_id ON public.users USING btree (parent_id);


--
-- Name: ix_users_tree_path; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_users_tree_path ON public.users USING btree (tree_path);


--
-- Name: ix_verification_attempts_email; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_verification_attempts_email ON public.verification_attempts USING btree (email);


--
-- Name: ix_wallet_user_id; Type: INDEX; Schema: public; Owner: doadmin
--

CREATE INDEX ix_wallet_user_id ON public.wallets USING btree (user_id);


--
-- Name: agents trigger_agent_commission_threshold; Type: TRIGGER; Schema: public; Owner: doadmin
--

CREATE TRIGGER trigger_agent_commission_threshold AFTER UPDATE OF paid_customers_count ON public.agents FOR EACH ROW WHEN ((new.is_active = true)) EXECUTE FUNCTION public.check_agent_commission_threshold();


--
-- Name: TRIGGER trigger_agent_commission_threshold ON agents; Type: COMMENT; Schema: public; Owner: doadmin
--

COMMENT ON TRIGGER trigger_agent_commission_threshold ON public.agents IS 'Auto-release commissions when agent reaches 10 customers';


--
-- Name: payment_methods trigger_payment_methods_updated_at; Type: TRIGGER; Schema: public; Owner: doadmin
--

CREATE TRIGGER trigger_payment_methods_updated_at BEFORE UPDATE ON public.payment_methods FOR EACH ROW EXECUTE FUNCTION public.update_payment_methods_updated_at();


--
-- Name: blog_posts trigger_update_blog_posts_updated_at; Type: TRIGGER; Schema: public; Owner: doadmin
--

CREATE TRIGGER trigger_update_blog_posts_updated_at BEFORE UPDATE ON public.blog_posts FOR EACH ROW EXECUTE FUNCTION public.update_blog_posts_updated_at();


--
-- Name: faqs trigger_update_faqs_updated_at; Type: TRIGGER; Schema: public; Owner: doadmin
--

CREATE TRIGGER trigger_update_faqs_updated_at BEFORE UPDATE ON public.faqs FOR EACH ROW EXECUTE FUNCTION public.update_faqs_updated_at();


--
-- Name: payment_approval_requests trigger_update_payment_approval_requests_updated_at; Type: TRIGGER; Schema: public; Owner: doadmin
--

CREATE TRIGGER trigger_update_payment_approval_requests_updated_at BEFORE UPDATE ON public.payment_approval_requests FOR EACH ROW EXECUTE FUNCTION public.update_payment_approval_requests_updated_at();


--
-- Name: support_tickets trigger_update_support_tickets_updated_at; Type: TRIGGER; Schema: public; Owner: doadmin
--

CREATE TRIGGER trigger_update_support_tickets_updated_at BEFORE UPDATE ON public.support_tickets FOR EACH ROW EXECUTE FUNCTION public.update_support_tickets_updated_at();


--
-- Name: affiliate_commissions affiliate_commissions_affiliate_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_commissions
    ADD CONSTRAINT affiliate_commissions_affiliate_user_id_fkey FOREIGN KEY (affiliate_user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: affiliate_commissions affiliate_commissions_payout_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_commissions
    ADD CONSTRAINT affiliate_commissions_payout_id_fkey FOREIGN KEY (payout_id) REFERENCES public.affiliate_payouts(id) ON DELETE SET NULL;


--
-- Name: affiliate_commissions affiliate_commissions_referral_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_commissions
    ADD CONSTRAINT affiliate_commissions_referral_id_fkey FOREIGN KEY (referral_id) REFERENCES public.affiliate_referrals(id) ON DELETE SET NULL;


--
-- Name: affiliate_links affiliate_links_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_links
    ADD CONSTRAINT affiliate_links_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: affiliate_payouts affiliate_payouts_affiliate_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_payouts
    ADD CONSTRAINT affiliate_payouts_affiliate_user_id_fkey FOREIGN KEY (affiliate_user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: affiliate_referrals affiliate_referrals_affiliate_link_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_referrals
    ADD CONSTRAINT affiliate_referrals_affiliate_link_id_fkey FOREIGN KEY (affiliate_link_id) REFERENCES public.affiliate_links(id) ON DELETE CASCADE;


--
-- Name: affiliate_referrals affiliate_referrals_affiliate_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_referrals
    ADD CONSTRAINT affiliate_referrals_affiliate_user_id_fkey FOREIGN KEY (affiliate_user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: affiliate_referrals affiliate_referrals_program_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_referrals
    ADD CONSTRAINT affiliate_referrals_program_id_fkey FOREIGN KEY (program_id) REFERENCES public.trading_programs(id) ON DELETE SET NULL;


--
-- Name: affiliate_referrals affiliate_referrals_referred_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_referrals
    ADD CONSTRAINT affiliate_referrals_referred_user_id_fkey FOREIGN KEY (referred_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: agents agents_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.agents
    ADD CONSTRAINT agents_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: blog_posts blog_posts_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.blog_posts
    ADD CONSTRAINT blog_posts_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: challenges challenges_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.challenges
    ADD CONSTRAINT challenges_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);


--
-- Name: challenges challenges_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.challenges
    ADD CONSTRAINT challenges_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: challenges challenges_program_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.challenges
    ADD CONSTRAINT challenges_program_id_fkey FOREIGN KEY (program_id) REFERENCES public.trading_programs(id);


--
-- Name: challenges challenges_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.challenges
    ADD CONSTRAINT challenges_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: commission_balances commission_balances_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commission_balances
    ADD CONSTRAINT commission_balances_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: commission_withdrawals commission_withdrawals_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commission_withdrawals
    ADD CONSTRAINT commission_withdrawals_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);


--
-- Name: commission_withdrawals commission_withdrawals_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commission_withdrawals
    ADD CONSTRAINT commission_withdrawals_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: commissions commissions_agent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commissions
    ADD CONSTRAINT commissions_agent_id_fkey FOREIGN KEY (agent_id) REFERENCES public.agents(id);


--
-- Name: commissions commissions_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commissions
    ADD CONSTRAINT commissions_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);


--
-- Name: commissions commissions_challenge_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commissions
    ADD CONSTRAINT commissions_challenge_id_fkey FOREIGN KEY (challenge_id) REFERENCES public.challenges(id);


--
-- Name: commissions commissions_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commissions
    ADD CONSTRAINT commissions_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: commissions commissions_referral_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commissions
    ADD CONSTRAINT commissions_referral_id_fkey FOREIGN KEY (referral_id) REFERENCES public.referrals(id);


--
-- Name: commissions commissions_rule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commissions
    ADD CONSTRAINT commissions_rule_id_fkey FOREIGN KEY (rule_id) REFERENCES public.commission_rules(id);


--
-- Name: commissions commissions_source_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commissions
    ADD CONSTRAINT commissions_source_user_id_fkey FOREIGN KEY (source_user_id) REFERENCES public.users(id);


--
-- Name: commissions commissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.commissions
    ADD CONSTRAINT commissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: email_queue email_queue_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.email_queue
    ADD CONSTRAINT email_queue_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: email_verification_tokens email_verification_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.email_verification_tokens
    ADD CONSTRAINT email_verification_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: affiliate_commissions fk_commission_payout; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.affiliate_commissions
    ADD CONSTRAINT fk_commission_payout FOREIGN KEY (payout_id) REFERENCES public.affiliate_payouts(id) ON DELETE SET NULL;


--
-- Name: lead_activities lead_activities_lead_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.lead_activities
    ADD CONSTRAINT lead_activities_lead_id_fkey FOREIGN KEY (lead_id) REFERENCES public.leads(id);


--
-- Name: lead_activities lead_activities_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.lead_activities
    ADD CONSTRAINT lead_activities_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: lead_notes lead_notes_lead_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.lead_notes
    ADD CONSTRAINT lead_notes_lead_id_fkey FOREIGN KEY (lead_id) REFERENCES public.leads(id);


--
-- Name: lead_notes lead_notes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.lead_notes
    ADD CONSTRAINT lead_notes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: leads leads_assigned_to_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.leads
    ADD CONSTRAINT leads_assigned_to_fkey FOREIGN KEY (assigned_to) REFERENCES public.users(id);


--
-- Name: leads leads_converted_to_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.leads
    ADD CONSTRAINT leads_converted_to_user_id_fkey FOREIGN KEY (converted_to_user_id) REFERENCES public.users(id);


--
-- Name: notification_preferences notification_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.notification_preferences
    ADD CONSTRAINT notification_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: password_reset_tokens password_reset_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: payment_approval_requests payment_approval_requests_challenge_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.payment_approval_requests
    ADD CONSTRAINT payment_approval_requests_challenge_id_fkey FOREIGN KEY (challenge_id) REFERENCES public.challenges(id) ON DELETE CASCADE;


--
-- Name: payment_approval_requests payment_approval_requests_payment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.payment_approval_requests
    ADD CONSTRAINT payment_approval_requests_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payments(id) ON DELETE CASCADE;


--
-- Name: payment_approval_requests payment_approval_requests_requested_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.payment_approval_requests
    ADD CONSTRAINT payment_approval_requests_requested_by_fkey FOREIGN KEY (requested_by) REFERENCES public.users(id);


--
-- Name: payment_approval_requests payment_approval_requests_requested_for_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.payment_approval_requests
    ADD CONSTRAINT payment_approval_requests_requested_for_fkey FOREIGN KEY (requested_for) REFERENCES public.users(id);


--
-- Name: payment_approval_requests payment_approval_requests_reviewed_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.payment_approval_requests
    ADD CONSTRAINT payment_approval_requests_reviewed_by_fkey FOREIGN KEY (reviewed_by) REFERENCES public.users(id);


--
-- Name: payment_methods payment_methods_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.payment_methods
    ADD CONSTRAINT payment_methods_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: payments payments_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);


--
-- Name: payments payments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: program_addons program_addons_program_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.program_addons
    ADD CONSTRAINT program_addons_program_id_fkey FOREIGN KEY (program_id) REFERENCES public.trading_programs(id);


--
-- Name: referrals referrals_agent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT referrals_agent_id_fkey FOREIGN KEY (agent_id) REFERENCES public.agents(id);


--
-- Name: referrals referrals_referred_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT referrals_referred_user_id_fkey FOREIGN KEY (referred_user_id) REFERENCES public.users(id);


--
-- Name: support_articles support_articles_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.support_articles
    ADD CONSTRAINT support_articles_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- Name: support_tickets support_tickets_assigned_to_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.support_tickets
    ADD CONSTRAINT support_tickets_assigned_to_fkey FOREIGN KEY (assigned_to) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: support_tickets support_tickets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.support_tickets
    ADD CONSTRAINT support_tickets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: tenants tenants_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.tenants
    ADD CONSTRAINT tenants_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.tenants(id);


--
-- Name: ticket_messages ticket_messages_ticket_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.ticket_messages
    ADD CONSTRAINT ticket_messages_ticket_id_fkey FOREIGN KEY (ticket_id) REFERENCES public.support_tickets(id) ON DELETE CASCADE;


--
-- Name: ticket_messages ticket_messages_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.ticket_messages
    ADD CONSTRAINT ticket_messages_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: trades trades_challenge_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.trades
    ADD CONSTRAINT trades_challenge_id_fkey FOREIGN KEY (challenge_id) REFERENCES public.challenges(id);


--
-- Name: trading_programs trading_programs_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.trading_programs
    ADD CONSTRAINT trading_programs_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenants(id);


--
-- Name: transactions transactions_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: transactions transactions_wallet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_wallet_id_fkey FOREIGN KEY (wallet_id) REFERENCES public.wallets(id);


--
-- Name: users users_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.users(id);


--
-- Name: users users_referred_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_referred_by_user_id_fkey FOREIGN KEY (referred_by_user_id) REFERENCES public.users(id);


--
-- Name: users users_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenants(id);


--
-- Name: wallets wallets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.wallets
    ADD CONSTRAINT wallets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: withdrawals withdrawals_agent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.withdrawals
    ADD CONSTRAINT withdrawals_agent_id_fkey FOREIGN KEY (agent_id) REFERENCES public.agents(id);


--
-- Name: withdrawals withdrawals_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: doadmin
--

ALTER TABLE ONLY public.withdrawals
    ADD CONSTRAINT withdrawals_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict PfqoKhBweiGF2u8biCMcHoOiCCIkQcdqbVCBbBNGXBkHJi3iWX8DnlblVaZGphy

